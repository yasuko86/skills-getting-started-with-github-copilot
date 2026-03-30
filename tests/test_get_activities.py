"""
Tests for GET /activities endpoint.

Tests follow AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and fixtures
- Act: Call the endpoint
- Assert: Validate response status, content, and data structure
"""


def test_get_all_activities_returns_success(client):
    """
    Arrange: Client fixture is ready
    Act: GET /activities
    Assert: Returns 200 with all activities
    """
    # Arrange - client is ready

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == 9


def test_get_activities_contains_all_activity_names(client):
    """
    Arrange: Expected activity names
    Act: GET /activities
    Assert: Response includes all expected activities
    """
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Studio",
        "Drama Club",
        "Robotics Club",
        "Science Olympiad"
    ]

    # Act
    response = client.get("/activities")

    # Assert
    activities = response.json()
    for activity_name in expected_activities:
        assert activity_name in activities


def test_activity_has_required_fields(client):
    """
    Arrange: Client fixture is ready
    Act: GET /activities
    Assert: Each activity has required fields
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    activities = response.json()
    for activity_name, activity_data in activities.items():
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required fields"
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_activity_participants_list_format(client):
    """
    Arrange: Client fixture is ready
    Act: GET /activities
    Assert: Participants are returned as emails in a list
    """
    # Arrange - client is ready

    # Act
    response = client.get("/activities")

    # Assert
    activities = response.json()
    for activity_name, activity_data in activities.items():
        participants = activity_data["participants"]
        assert isinstance(participants, list)
        for participant in participants:
            assert "@" in participant, f"Participant '{participant}' is not a valid email"
