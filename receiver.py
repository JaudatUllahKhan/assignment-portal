
from flask import Flask, request, jsonify
import json
from pathlib import Path

receiver = Flask(__name__)

REPORT_FILE = Path(__file__).parent / "test-report.json"


@receiver.route("/report", methods=["POST"])
def receive_report():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Invalid JSON report"
        }), 400

    required = [
        "repository",
        "branch",
        "commit_sha",
        "run_id",
        "timestamp",
        "tests",
        "total",
        "passed",
        "failed",
        "status"
    ]

    missing = [key for key in required if key not in data]

    if missing:
        return jsonify({
            "error": "Missing fields",
            "fields": missing
        }), 400

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Test report received and saved!", flush=True)

    return jsonify({
        "message": "Report saved successfully",
        "file": "test-report.json"
    }), 200


if __name__ == "__main__":
    receiver.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )
