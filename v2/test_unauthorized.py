import pytest
import requests
from datetime import datetime
from config import BASE_URL, HEADERS


def test_get_deals_green():
    """Test GET request to fetch deals"""
    endpoint = "/api/v2/GetDeals/example2.com"
    params = {"isVerified": "true", "category": "Sport"}

    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params)

    # data = response.json()
    assert response.status_code == 200
    assert response.text == ""
