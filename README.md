
# Assignment Submission Portal

## CSC418 - DevOps Lab Midterm Project

An assignment submission portal developed using Python Flask and integrated with GitHub Actions for automated testing, test reporting, conditional deployment, and email notifications.

## Project Features

- Submit assignments using a web form
- Enter student name, registration number, assignment title, and submission URL
- Validate required fields and submission URLs
- Store assignment records in SQLite
- Display submitted assignments
- Run automated tests using pytest
- Generate and deliver JSON test reports
- Automatically deploy the static demo to GitHub Pages
- Send Gmail notifications for passing and failing tests

## Technologies Used

- Python
- Flask
- SQLite
- HTML, CSS, JavaScript
- pytest
- Git and GitHub
- GitHub Actions
- Windows self-hosted runner
- GitHub Pages
- Gmail SMTP

## Project Structure

    assignment-portal/
    |
    |-- app.py
    |-- test_app.py
    |-- receiver.py
    |-- send_report.py
    |-- send_email.py
    |-- requirements.txt
    |-- README.md
    |
    |-- docs/
    |   |-- index.html
    |
    |-- .github/
        |-- workflows/
            |-- ci.yml

## Run the Flask Application

Install dependencies:

    python -m pip install -r requirements.txt

Start the application:

    python app.py

Open the local address displayed in the terminal.

## Automated Testing

Run the three application tests:

    python -m pytest test_app.py -v

The automated tests verify:

1. Valid assignment submission
2. Missing registration number validation
3. Invalid submission URL validation

## Continuous Integration

GitHub Actions automatically runs the test workflow whenever changes are pushed to the main branch.

The workflow:

1. Checks out the repository
2. Installs Python dependencies
3. Executes automated tests
4. Generates pytest-results.xml
5. Sends a JSON report to the local receiver
6. Sends a Gmail notification
7. Deploys GitHub Pages only when tests pass

## Local JSON Test Reporting

Start the HTTP receiver:

    python receiver.py

The receiver listens at:

    http://127.0.0.1:5001/report

The Windows self-hosted GitHub Actions runner sends test results to this endpoint.

The receiver saves the latest report in:

    test-report.json

The report contains:

- Repository and branch
- Commit SHA
- Workflow run ID
- Timestamp
- Individual test results
- Failure messages
- Passed, failed, and skipped counts
- Overall status

## Passing and Failing Test Demonstration

The CI pipeline was tested under three conditions:

1. All three tests passed
2. A deliberate test failure was introduced and detected
3. The original code was restored and the tests passed again

The failing workflow prevented GitHub Pages deployment.

## GitHub Pages Deployment

GitHub Pages deployment is conditional.

The deployment job runs only after the test job succeeds.

Live static demo:

https://jaudatullahkhan.github.io/assignment-portal/

Note: The GitHub Pages demo uses browser localStorage.
The Flask application uses SQLite and runs separately.

## Automatic Gmail Reporting

The workflow sends email notifications for both successful and failed test runs.

Each email includes:

- Overall test status
- Repository and branch
- Commit SHA
- Workflow run ID
- Passed, failed, and skipped test counts
- Failure details
- GitHub Actions run link

Gmail credentials are stored securely using GitHub Actions Secrets:

- GMAIL_USERNAME
- GMAIL_APP_PASSWORD
- REPORT_EMAIL

No email passwords are stored in the source code.

## GitHub Repository

https://github.com/JaudatUllahKhan/assignment-portal

## Conclusion

This project demonstrates the practical implementation of DevOps concepts, including version control, continuous integration, automated testing, test reporting, conditional deployment, and automated notifications.

GitHub Actions provides a complete workflow that detects application errors, reports test results, and publishes the website only after successful testing.
