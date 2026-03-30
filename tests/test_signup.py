"""
Tests for POST /activities/{activity_name}/signup endpoint.

Tests follow AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and mock activities
- Act: Make signup request
- Assert: Validate response and database state changes
"""

import pytest


def test_successful_signup_adds_participant(client, common_emails, monkeypatch):
    """
    Arrange: Fresh activities, new student email
    Act: POST signup for ChessClub
    Assert: Returns 200, participant added to list
    """
    # Arrange
    from src import app as app_module
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)
    
    email = common_emails["new_student"]
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert email in fresh_activities[activity_name]["participants"]
    assert "Signed up" in response.json()["message"]
    assert len(fresh_activities[activity_name]["participants"]) == 2


def test_duplicate_signup_returns_400(client, common_emails, monkeypatch):
    """
    Arrange: Fresh activities, student already signed up for Chess Club
    Act: POST duplicate signup request
    Assert: Returns 400 error, participant list unchanged
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
    response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    assert len(fresh_activities["Chess Club"]["participants"]) == 1


def test_signup_nonexistent_activity_returns_404(client, common_emails, monkeypatch):
    """
    Arrange: Fresh activities with no "Nonexistent Club"
    Act: POST signup for non-existent activity
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
    
    email = common_emails["new_student"]

    # Act
    response = client.post(
        "/activities/Nonexistent Club/signup?email={email}"
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_response_contains_confirmation_message(client, common_emails, monkeypatch):
    """
    Arrange: Fresh activities, new student email
    Act: POST successful signup
    Assert: Response contains confirmation message with email and activity
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
    
    email = common_emails["new_student"]

    # Act
    response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    message = response.json()["message"]
    assert email in message
    assert "Chess Club" in message


def test_signup_with_special_characters_in_email(client, monkeypatch):
    """
    Arrange: Fresh activities, email with special characters (valid format)
    Act: POST signup with special-char email (URL encoded)
    Assert: Returns 200, participant added
    """
    # Arrange
    from src import app as app_module
    from urllib.parse import urlencode
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": []
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)
    
    email = "test+coding@mergington.edu"

    # Act - properly URL encode the email parameter
    response = client.post(
        f"/activities/Chess Club/signup?{urlencode({'email': email})}"
    )

    # Assert
    assert response.status_code == 200
    assert email in fresh_activities["Chess Club"]["participants"]


def test_signup_participant_count_increments(client, common_emails, monkeypatch):
    """
    Arrange: Fresh activities with 1 existing participant
    Act: POST signup for new student
    Assert: Participant count increases by 1
    """
    # Arrange
    from src import app as app_module
    fresh_activities = {
        "Chess Club": {
            "description": "Learn chess",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["existing@mergington.edu"]
        }
    }
    monkeypatch.setattr(app_module, "activities", fresh_activities)
    
    initial_count = len(fresh_activities["Chess Club"]["participants"])
    email = common_emails["new_student"]

    # Act
    response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert len(fresh_activities["Chess Club"]["participants"]) == initial_count + 1
