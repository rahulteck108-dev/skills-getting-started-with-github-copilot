"""
Tests for activities listing endpoint (GET /activities)
Using AAA (Arrange-Act-Assert) pattern for clarity and consistency.
"""


def test_get_activities_returns_all(client):
    """
    Test that GET /activities returns all activities
    
    AAA Pattern:
    - Arrange: 9 test activities loaded via fixture
    - Act: Send GET request to /activities
    - Assert: Verify 200 status and all 9 activities in response
    """
    # Arrange
    # client fixture already contains 9 activities
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class",
        "Basketball Team", "Tennis Club", "Art Studio",
        "Drama Club", "Debate Club", "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    for activity_name in expected_activities:
        assert activity_name in data


def test_get_activities_structure(client):
    """
    Test that each activity has the required fields
    
    AAA Pattern:
    - Arrange: Test data ready
    - Act: Send GET request to /activities
    - Assert: Verify each activity has description, schedule, max_participants, participants
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_includes_participants(client):
    """
    Test that participants list is correctly populated
    
    AAA Pattern:
    - Arrange: Chess Club has 2 participants in test data
    - Act: Send GET request to /activities
    - Assert: Verify Chess Club's participants list is correct
    """
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    chess_club = data["Chess Club"]
    
    assert len(chess_club["participants"]) == 2
    assert chess_club["participants"] == expected_chess_participants
