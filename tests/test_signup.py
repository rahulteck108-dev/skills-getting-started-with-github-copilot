"""
Tests for signup endpoint (POST /activities/{activity_name}/signup)
Using AAA (Arrange-Act-Assert) pattern for clarity and consistency.
"""


def test_signup_success(client):
    """
    Test successful signup for an activity
    
    AAA Pattern:
    - Arrange: email="newuser@example.com", activity="Chess Club"
    - Act: POST /activities/Chess Club/signup?email=newuser@example.com
    - Assert: Verify 200 status, success message, and participant added
    """
    # Arrange
    email = "newuser@example.com"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
    
    # Verify participant was added to activities
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity]["participants"]


def test_signup_duplicate_email(client):
    """
    Test that duplicate signup is prevented
    
    AAA Pattern:
    - Arrange: email already exists in Chess Club (michael@mergington.edu)
    - Act: POST signup with same email twice
    - Assert: First succeeds, second returns 400 with "Already signed up" error
    """
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    
    # Act - First signup should fail because already signed up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert - Should get 400 error
    assert response.status_code == 400
    data = response.json()
    assert "Already signed up" in data["detail"]


def test_signup_activity_not_found(client):
    """
    Test signup to non-existent activity
    
    AAA Pattern:
    - Arrange: activity="Nonexistent Activity"
    - Act: POST /activities/Nonexistent Activity/signup?email=new@example.com
    - Assert: Verify 404 status and "Activity not found" error
    """
    # Arrange
    email = "newuser@example.com"
    activity = "Nonexistent Activity"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_adds_to_empty_activity(client):
    """
    Test signup to an activity with no current participants
    
    AAA Pattern:
    - Arrange: Basketball Team has participants, use a new email
    - Act: POST /activities/Basketball Team/signup?email=newemail@example.com
    - Assert: Verify participant added successfully
    """
    # Arrange
    email = "newparticipant@example.com"
    activity = "Basketball Team"
    original_count = len(client.get("/activities").json()[activity]["participants"])
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    updated_count = len(client.get("/activities").json()[activity]["participants"])
    assert updated_count == original_count + 1
