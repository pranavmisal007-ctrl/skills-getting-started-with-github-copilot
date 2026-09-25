from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity = "Chess Club"
    email = "delete-test-student@mergington.edu"

    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert delete_response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
