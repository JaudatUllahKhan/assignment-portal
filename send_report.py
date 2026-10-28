
import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# Read actual pytest results
tree = ET.parse("pytest-results.xml")
root = tree.getroot()

tests = []

for case in root.iter("testcase"):
    failure = case.find("failure")
    error = case.find("error")
    skipped = case.find("skipped")

    problem = failure if failure is not None else error

    if problem is not None:
        result = "failed"
        message = problem.get("message") or problem.text or ""
    elif skipped is not None:
        result = "skipped"
        message = skipped.get("message") or ""
    else:
        result = "passed"
        message = None

    tests.append({
        "name": case.get("name"),
        "result": result,
        "failure_message": message
    })

passed = sum(t["result"] == "passed" for t in tests)
failed = sum(t["result"] == "failed" for t in tests)
skipped = sum(t["result"] == "skipped" for t in tests)

report = {
    "repository": os.getenv("GITHUB_REPOSITORY", ""),
    "branch": os.getenv("GITHUB_REF_NAME", ""),
    "commit_sha": os.getenv("GITHUB_SHA", ""),
    "run_id": os.getenv("GITHUB_RUN_ID", ""),
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": tests,
    "total": len(tests),
    "passed": passed,
    "failed": failed,
    "skipped": skipped,
    "status": "passed" if failed == 0 and passed > 0 else "failed"
}

payload = json.dumps(report).encode("utf-8")

request = urllib.request.Request(
    "http://127.0.0.1:5001/report",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(request, timeout=15) as response:
    print("Report delivery:", response.status)

print(json.dumps(report, indent=2))
