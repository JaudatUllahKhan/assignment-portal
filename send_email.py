
import os
import smtplib
import ssl
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.message import EmailMessage

REPORT_FILE = "pytest-results.xml"


def read_test_results():
    if not os.path.exists(REPORT_FILE):
        return {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "status": "ERROR",
            "details": "Test results file was not generated.",
        }

    root = ET.parse(REPORT_FILE).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall(".//testsuite")

    cases = []
    for suite in suites:
        cases.extend(suite.findall("testcase"))

    total = len(cases)
    failed = 0
    skipped = 0
    failure_details = []

    for case in cases:
        name = case.get("name", "Unknown test")
        failure = case.find("failure")
        error = case.find("error")

        if failure is not None or error is not None:
            failed += 1
            problem = failure if failure is not None else error
            message = problem.get("message") or problem.text or "Unknown failure"
            failure_details.append(f"{name}: {message.strip()}")

        elif case.find("skipped") is not None:
            skipped += 1

    passed = total - failed - skipped

    status = "PASSED" if total > 0 and failed == 0 else "FAILED"

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "status": status,
        "details": "\n\n".join(failure_details) or "No test failures.",
    }


def send_email():
    username = os.environ["GMAIL_USERNAME"]
    password = os.environ["GMAIL_APP_PASSWORD"].replace(" ", "")
    recipient = os.environ["REPORT_EMAIL"]

    results = read_test_results()

    repository = os.getenv("GITHUB_REPOSITORY", "assignment-portal")
    branch = os.getenv("GITHUB_REF_NAME", "main")
    commit = os.getenv("GITHUB_SHA", "Local execution")
    run_id = os.getenv("GITHUB_RUN_ID", "N/A")
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    run_url = (
        f"https://github.com/{repository}/actions/runs/{run_id}"
        if run_id != "N/A" else "N/A"
    )

    body = f"""ASSIGNMENT PORTAL - AUTOMATED TEST REPORT

Overall Status: {results['status']}

Repository: {repository}
Branch: {branch}
Commit: {commit}
Workflow Run ID: {run_id}
Timestamp: {timestamp}

TEST RESULTS
------------------------------
Total: {results['total']}
Passed: {results['passed']}
Failed: {results['failed']}
Skipped: {results['skipped']}

FAILURE DETAILS
------------------------------
{results['details']}

GitHub Actions Run:
{run_url}

This email was generated automatically by GitHub Actions.
"""

    message = EmailMessage()
    message["Subject"] = f"[Assignment Portal CI] {results['status']} - Run #{run_id}"
    message["From"] = username
    message["To"] = recipient
    message.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=30) as smtp:
        smtp.login(username, password)
        smtp.send_message(message)

    print(f"Email report sent successfully. Status: {results['status']}")


if __name__ == "__main__":
    send_email()
