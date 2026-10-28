
import pytest
import app as portal


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a separate database for each test
    test_database = tmp_path / "test_submissions.db"
    monkeypatch.setattr(
        portal, "DATABASE", str(test_database)
    )

    portal.app.config["TESTING"] = True
    portal.init_db()

    with portal.app.test_client() as client:
        yield client


def test_valid_submission(client):
    response = client.post("/", data={
        "name": "Ali Khan",
        "registration": "FA23-BSE-001",
        "title": "DevOps Lab Midterm",
        "url": "https://github.com/example/project"
    })

    assert response.status_code == 200
    assert b"Assignment submitted successfully!" in response.data
    assert b"Ali Khan" in response.data
    assert b"FA23-BSE-001" in response.data

    with portal.get_connection() as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM submissions"
        ).fetchone()[0]

    assert count == 1


def test_missing_registration(client):
    response = client.post("/", data={
        "name": "Ali Khan",
        "registration": "",
        "title": "DevOps Lab Midterm",
        "url": "https://github.com/example/project"
    })

    assert response.status_code == 200
    assert b"All fields are required." in response.data

    with portal.get_connection() as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM submissions"
        ).fetchone()[0]

    assert count == 0


def test_invalid_url(client):
    response = client.post("/", data={
        "name": "Ali Khan",
        "registration": "FA23-BSE-001",
        "title": "DevOps Lab Midterm",
        "url": "invalid-url"
    })

    assert response.status_code == 200
    assert b"Invalid submission URL." in response.data

    with portal.get_connection() as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM submissions"
        ).fetchone()[0]

    assert count == 0
