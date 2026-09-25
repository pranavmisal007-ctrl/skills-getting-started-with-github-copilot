import uuid

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def make_email(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}@mergington.edu"


def test_signup_adds_participant_to_activity():
    activity = "Chess Club"
    email = make_email("signup")

    response = client.post(f"/activities/{activity}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_duplicate_signup_is_rejected():
    activity = "Chess Club"
    email = make_email("duplicate")

    first_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert first_response.status_code == 200

    duplicate_response = client.post(f"/activities/{activity}/signup?email={email}")

    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()


def test_unregister_participant_removes_email_from_activity():
    activity = "Chess Club"
    email = make_email("delete")

    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert delete_response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
