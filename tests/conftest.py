"""
Pytest configuration and shared fixtures for Mergington High School API tests.

This module provides:
- FastAPI TestClient for making test requests
- Fresh activities database fixture (deepcopy for test isolation)
- Common test email fixtures
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a FastAPI TestClient for making HTTP requests to the app."""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Provide a fresh copy of the activities database for each test.
    Uses deepcopy to ensure test isolation - modifications don't affect other tests.
    """
    activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and practice",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Recreational and competitive soccer",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and visual arts",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater productions and acting workshops",
            "schedule": "Thursdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu", "grace@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots for competitions",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["liam@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science challenges and tournaments",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "mason@mergington.edu"]
        }
    }
    
    return copy.deepcopy(activities)


@pytest.fixture
def common_emails():
    """Provide common test email addresses."""
    return {
        "new_student": "newstudent@mergington.edu",
        "existing_chess": "michael@mergington.edu",
        "existing_programming": "emma@mergington.edu",
        "test_email": "test@mergington.edu"
    }
