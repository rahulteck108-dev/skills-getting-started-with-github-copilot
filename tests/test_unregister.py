"""
Tests for unregister endpoint (DELETE /activities/{activity_name}/unregister)
Using AAA (Arrange-Act-Assert) pattern for clarity and consistency.
"""


def test_unregister_success(client):
    """
    Test successful unregister from an activity
    
    AAA Pattern:
    - Arrange: Chess Club has participants, email="michael@mergington.edu"
    - Act: DELETE /activities/Chess Club/unregister?email=michael@mergington.edu
    - Assert: Verify 200 status, success message, and participant removed
    """
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Verify participant exists before unregister
    activities_before = client.get("/activities").json()
    assert email in activities_before[activity]["participants"]
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Unregistered" in data["message"]
    
    # Verify participant was removed from activities
    activities_after = client.get("/activities").json()
    assert email not in activities_after[activity]["participants"]


def test_unregister_participant_not_found(client):
    """
    Test unregister with non-existent participant
    
    AAA Pattern:
    - Arrange: email="nonexistent@example.com" not in any activity
    - Act: DELETE /activities/Chess Club/unregister?email=nonexistent@example.com
    - Assert: Verify 404 status and "Participant not found" error
    """
    # Arrange
    email = "nonexistent@example.com"
    activity = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found in this activity" in data["detail"]


def test_unregister_activity_not_found(client):
    """
    Test unregister from non-existent activity
    
    AAA Pattern:
    - Arrange: activity="Nonexistent Activity"
    - Act: DELETE /activities/Nonexistent Activity/unregister?email=any@example.com
    - Assert: Verify 404 status and "Activity not found" error
    """
    # Arrange
    email = "anyuser@example.com"
    activity = "Nonexistent Activity"
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_multiple_participants(client):
    """
    Test unregistering one participant doesn't affect others
    
    AAA Pattern:
    - Arrange: Chess Club has 2 participants, unregister one
    - Act: DELETE /activities/Chess Club/unregister?email=michael@mergington.edu
    - Assert: michael is removed, daniel remains
    """
    # Arrange
    email_to_remove = "michael@mergington.edu"
    email_to_remain = "daniel@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email_to_remove}")
    
    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    
    assert email_to_remove not in activities[activity]["participants"]
    assert email_to_remain in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == 1
