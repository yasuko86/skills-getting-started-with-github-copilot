"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint.

Tests follow AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and mock activities
- Act: Make delete request
- Assert: Validate response and database state changes
"""

import pytest


def test_successful_unregister_removes_participant(client, common_emails, monkeypatch):
    """
    Arrange: Fresh activities with participant to remove
    Act: DELETE participant from activity
    Assert: Returns 200, participant removed from list
    """
    # Arrange
    from src import app as app_module
    email = common_emails["existing_chess"]
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": [email, "other@mergington.edu"]
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)

    # Act
    response = client.delete(
        f"/activities/Chess Club/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    assert email not in fresh_activities["Chess Club"]["participants"]
    assert len(fresh_activities["Chess Club"]["participants"]) == 1


def test_unregister_nonexistent_participant_returns_400(client, monkeypatch):
    """
    Arrange: Fresh activities, email not in participants
    Act: DELETE participant not signed up
    Assert: Returns 400 error, list unchanged
    """
    # Arrange
    from src import app as app_module
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["other@mergington.edu"]
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)
    
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/Chess Club/participants/{email}"
    )

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()
    assert len(fresh_activities["Chess Club"]["participants"]) == 1


def test_unregister_nonexistent_activity_returns_404(client, monkeypatch):
    """
    Arrange: Fresh activities with no "Nonexistent Club"
    Act: DELETE from non-existent activity
    Assert: Returns 404 error
    """
    # Arrange
    from src import app as app_module
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": []
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)
    
    email = "test@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/Nonexistent Club/participants/{email}"
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_response_contains_confirmation(client, common_emails, monkeypatch):
    """
    Arrange: Fresh activities with participant
    Act: DELETE successful unregister
    Assert: Response contains confirmation message
    """
    # Arrange
    from src import app as app_module
    email = common_emails["existing_chess"]
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": [email]
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)

    # Act
    response = client.delete(
        f"/activities/Chess Club/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    message = response.json()["message"]
    assert email in message
    assert "Chess Club" in message


def test_unregister_participant_count_decrements(client, common_emails, monkeypatch):
    """
    Arrange: Fresh activities with 3 participants
    Act: DELETE one participant
    Assert: Participant count decreases by 1
    """
    # Arrange
    from src import app as app_module
    email_to_remove = common_emails["existing_chess"]
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": [
                email_to_remove,
                "participant2@mergington.edu",
                "participant3@mergington.edu"
            ]
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)
    
    initial_count = len(fresh_activities["Chess Club"]["participants"])

    # Act
    response = client.delete(
        f"/activities/Chess Club/participants/{email_to_remove}"
    )

    # Assert
    assert response.status_code == 200
    assert len(fresh_activities["Chess Club"]["participants"]) == initial_count - 1


def test_unregister_with_url_encoded_email(client, monkeypatch):
    """
    Arrange: Fresh activities with email containing special characters
    Act: DELETE with URL-encoded email
    Assert: Returns 200, participant removed
    """
    # Arrange
    from src import app as app_module
    email = "test+code@mergington.edu"
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": [email]
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)

    # Act - FastAPI TestClient handles URL encoding
    response = client.delete(
        f"/activities/Chess Club/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    assert email not in fresh_activities["Chess Club"]["participants"]


def test_unregister_another_participant_remains(client, monkeypatch):
    """
    Arrange: Fresh activities with 2 participants
    Act: DELETE first participant
    Assert: Second participant remains unchanged
    """
    # Arrange
    from src import app as app_module
    email_to_remove = "participant1@mergington.edu"
    email_to_keep = "participant2@mergington.edu"
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": [email_to_remove, email_to_keep]
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)

    # Act
    response = client.delete(
        f"/activities/Chess Club/participants/{email_to_remove}"
    )

    # Assert
    assert response.status_code == 200
    assert email_to_remove not in fresh_activities["Chess Club"]["participants"]
    assert email_to_keep in fresh_activities["Chess Club"]["participants"]
