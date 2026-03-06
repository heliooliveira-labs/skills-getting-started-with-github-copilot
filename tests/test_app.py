import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@mergington.edu for Chess Club" in data["message"]
    
    # Verify participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=duplicate@mergington.edu")
    
    # Try to signup again
    response = client.post("/activities/Programming%20Class/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up" in data["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_from_activity():
    # First signup
    client.post("/activities/Gym%20Class/signup?email=unregister@mergington.edu")
    
    # Unregister
    response = client.post("/activities/Gym%20Class/unregister?email=unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@mergington.edu from Gym Class" in data["message"]
    
    # Verify participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@mergington.edu" not in data["Gym Class"]["participants"]

def test_unregister_nonexistent_participant():
    response = client.post("/activities/Chess%20Club/unregister?email=nonexistent@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Student not found in activity" in data["detail"]

def test_unregister_nonexistent_activity():
    response = client.post("/activities/Nonexistent%20Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]