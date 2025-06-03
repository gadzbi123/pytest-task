import pytest
import requests
from config import BASE_URL, HEADERS

def test_create_deal():
    """Test POST request to create a new deal"""
    endpoint = "/api/v2/Deals/"
    payload = {
        "title": "Test Deal",
        "description": "Test Description",
        "category": "Sport",
        "isVerified": True
    }
    
    response = requests.post(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
        json=payload
    )
    
    assert response.status_code in [200, 201]
    return response.json().get("id")  # Return the created deal ID for other tests

def test_update_deal():
    """Test PUT request to update a deal"""
    # First create a deal
    deal_id = test_create_deal()
    
    endpoint = f"/api/v2/Deals/{deal_id}"
    payload = {
        "title": "Updated Test Deal",
        "description": "Updated Test Description",
        "category": "Sport",
        "isVerified": True
    }
    
    response = requests.put(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
        json=payload
    )
    
    assert response.status_code == 200
    assert response.json().get("title") == "Updated Test Deal"

def test_delete_deal():
    """Test DELETE request to remove a deal"""
    # First create a deal
    deal_id = test_create_deal()
    
    endpoint = f"/api/v2/Deals/{deal_id}"
    
    response = requests.delete(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS
    )
    
    assert response.status_code in [200, 204]
    
    # Verify the deal is deleted
    get_response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS
    )
    assert get_response.status_code == 404 