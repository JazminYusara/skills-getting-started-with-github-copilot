from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_updates_activity_participants_immediately():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

    client.delete("/activities/Chess Club/participants/newstudent@mergington.edu")


def test_unregister_participant_removes_email_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )
