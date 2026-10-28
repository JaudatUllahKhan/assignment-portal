
import sqlite3
from urllib.parse import urlparse
from flask import Flask, request, render_template_string

app = Flask(__name__)
DATABASE = "submissions.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                registration TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL
            )
        """)


def valid_url(url):
    parsed = urlparse(url)
    return (
        parsed.scheme in ("http", "https")
        and bool(parsed.hostname)
        and "." in parsed.hostname
        and " " not in url
    )


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Assignment Submission Portal</title>
    <style>
        body {
            font-family: Arial;
            background: #f0f4f8;
            margin: 40px;
        }
        .container {
            max-width: 850px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 10px;
        }
        input, button {
            padding: 10px;
            margin: 7px 0;
            width: 100%;
            box-sizing: border-box;
        }
        button {
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
        }
        .error { color: red; }
        .success { color: green; }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Assignment Submission Portal</h1>

    <form method="POST">
        <input name="name" placeholder="Student Name">
        <input name="registration"
               placeholder="Registration Number">
        <input name="title" placeholder="Assignment Title">
        <input name="url" placeholder="Submission URL">
        <button type="submit">Submit Assignment</button>
    </form>

    <p class="{{ category }}">{{ message }}</p>

    <h2>Saved Submissions</h2>
    <table>
        <tr>
            <th>Name</th>
            <th>Registration</th>
            <th>Assignment</th>
            <th>URL</th>
        </tr>
        {% for s in submissions %}
        <tr>
            <td>{{ s[1] }}</td>
            <td>{{ s[2] }}</td>
            <td>{{ s[3] }}</td>
            <td>
                <a href="{{ s[4] }}" target="_blank"
                   rel="noopener noreferrer">
                    View Submission
                </a>
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    category = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        registration = request.form.get(
            "registration", ""
        ).strip()
        title = request.form.get("title", "").strip()
        url = request.form.get("url", "").strip()

        if not all([name, title, url]):
            message = "All fields are required."
            category = "error"

        elif not valid_url(url):
            message = "Invalid submission URL."
            category = "error"

        else:
            with get_connection() as conn:
                conn.execute(
                    """INSERT INTO submissions
                       (name, registration, title, url)
                       VALUES (?, ?, ?, ?)""",
                    (name, registration, title, url)
                )

            message = "Assignment submitted successfully!"
            category = "success"

    with get_connection() as conn:
        submissions = conn.execute(
            "SELECT * FROM submissions ORDER BY id DESC"
        ).fetchall()

    return render_template_string(
        HTML,
        submissions=submissions,
        message=message,
        category=category
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
