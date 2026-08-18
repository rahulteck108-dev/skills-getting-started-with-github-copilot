"""
Pytest configuration and fixtures for FastAPI tests.
Provides TestClient and test data isolation for all test modules.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app
import src.app as app_module


@pytest.fixture
def test_activities():
    """
    Fixture that provides a fresh copy of test activities data.
    Ensures test isolation - each test gets its own data without side effects.
    """
    return {
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
            "description": "Join our competitive basketball team and play in intramural tournaments",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis techniques and compete in friendly matches",
            "schedule": "Wednesdays and Saturdays, 10:00 AM - 11:30 AM",
            "max_participants": 12,
            "participants": ["sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture with guidance from experienced artists",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu", "lucas@mergington.edu", "nina@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in plays, musicals, and theatrical productions",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["tyler@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop public speaking and critical thinking skills through structured debates",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["sophia@mergington.edu", "brandon@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments, learn about scientific discoveries, and participate in science fairs",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["avery@mergington.edu"]
        }
    }


@pytest.fixture
def client(test_activities):
    """
    Fixture that provides a TestClient with patched activities data.
    Patches the app's in-memory activities dict with test data before each test.
    Returns to original state after test completes.
    """
    # Save the original activities
    original_activities = app_module.activities.copy()
    
    # Patch with test data
    app_module.activities.clear()
    app_module.activities.update(test_activities)
    
    # Create and return client
    test_client = TestClient(app)
    
    yield test_client
    
    # Restore original activities after test
    app_module.activities.clear()
    app_module.activities.update(original_activities)
