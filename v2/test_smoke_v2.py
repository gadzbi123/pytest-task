import pytest
import requests
from datetime import datetime
from config import BASE_URL, HEADERS, MERCHANTS_ARRAY
from utils import utils


def test_smoke_green():
    endpoint = "/api/v2/CreateDeal"
    get_params = {"isVerified": "true", "category": "Sport"}
    params = {
        "title": "Old Title",
        "description": "Old title desc",
        "domain": "example2.com",
        "code": "SAVE20",
        "expiresAt": "2025-12-31T23:59:59Z",
    }
    response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=params)
    print(response.text)
    assert response.status_code == 201
    data = response.json()
    dealId = data.get("dealId")
    assert utils.Is_uuid(dealId), f"{dealId} didn't match regex"

    # endpoint = f"/api/v2/GetDeal/{dealId}"
    # response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    # assert response.status_code == 200
    # assert response.json()

    params = {
        "title": "New Title",
        "description": "New title desc",
        "expiresAt": "2030-12-31T23:59:59Z",
    }
    endpoint = f"/api/v2/UpdateDeal/{dealId}"
    response = requests.put(f"{BASE_URL}{endpoint}", headers=HEADERS, json=params)
    assert response.status_code == 204
    assert response.text == ""

    endpoint = f"/api/v2/DeleteDeal/{dealId}"
    response = requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)
    assert response.status_code == 204
    assert response.text == ""


def test_get_deals_green():
    """Test GET request to fetch deals"""
    endpoint = "/api/v2/GetDeals/example.com"
    params = {"isVerified": "true", "category": "Sport"}

    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params)

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, (list, dict))
    assert data.get("count") == 0
    assert data.get("deals") == []


def test_get_deal_green():
    """Test GET request to fetch deal"""
    endpoint = "/api/v2/GetDeal/1b442cb336add37e8375070627efe751"
    params = {"isVerified": "true", "category": "Sport"}

    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params)

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, (list, dict))
    assert data.get("category") == "Electronics"
    assert data.get("code") == "HOLIDAY10"
    assert data.get("domain") == "asus.com"
    assert data.get("description") == "Take $100 off with coupon code on $100+ orders"
    assert data.get("title") == "$10 Off Orders over $100 at A.U. Store"
    assert data.get("id") == "1b442cb336add37e8375070627efe751"
    timestamp_created = data.get("createdAt")
    timestamp_modified = data.get("modifiedAt")
    timestamp_expires = data.get("expiresAt")

    # TODO Regression?
    assert timestamp_expires is None

    assert (
        datetime.fromisoformat("2023-12-05T16:00:00+00:00")
        < datetime.fromisoformat(timestamp_created)
        < datetime.fromisoformat("2023-12-05T16:02:00+00:00")
    ), "deal has unexpected time of creation"

    # TODO bad formatting
    assert datetime.fromisoformat(timestamp_created) <= datetime.fromisoformat(
        timestamp_modified
    ), "deals can't have modification date older than creation date"

    # assert datetime.fromisoformat(timestamp_created) <= datetime.fromisoformat(
    #     timestamp_expires
    # ), "deals can't have expiration date older than creation date"


def test_update_on_non_existing():
    non_existing_id = "00000000000000000000000000000000"
    params = {
        "title": "New Title",
        "description": "New title desc",
        "expiresAt": "2030-12-31T23:59:59Z",
    }
    endpoint = f"/api/v2/UpdateDeal/{non_existing_id}"
    response = requests.put(f"{BASE_URL}{endpoint}", headers=HEADERS, json=params)
    assert response.status_code == 404
    assert response.text == f"Deal with id '{non_existing_id}' not found."


def test_delete_on_non_existing():
    non_existing_id = "00000000000000000000000000000000"
    endpoint = f"/api/v2/DeleteDeal/{non_existing_id}"
    response = requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)
    assert response.status_code == 404
    assert response.text == f"Deal with id '{non_existing_id}' not found."


def test_merchants():
    endpoint = f"/api/v2/GetMerchants"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data.get("count") == 8
    assert data.get("merchants") == MERCHANTS_ARRAY
