"""
Tests for root endpoint (GET /)
Using AAA (Arrange-Act-Assert) pattern for clarity and consistency.
"""

from fastapi.testclient import TestClient


def test_root_redirects_to_index(client):
    """
    Test that GET / redirects to /static/index.html
    
    AAA Pattern:
    - Arrange: TestClient ready with test data
    - Act: Send GET request to /
    - Assert: Verify 307 status and correct location header
    """
    # Arrange
    # client fixture already provided by conftest.py
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
