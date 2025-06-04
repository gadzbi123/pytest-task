import pytest
import requests
from datetime import datetime
from config import BASE_URL, HEADERS, MERCHANTS_ARRAY
from utils import utils


def test_smoke_green():
    endpoint = "/api/v1/CreateDeal"
    params = {
        "title": "Old Title",
        "description": "Old title desc",
        "domain": "example.com",
        "code": "SAVE20",
        "expiresAt": "2025-12-31T23:59:59+00:00",
    }
    response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=params)
    print(response.text)
    assert response.status_code == 201
    data = response.json()
    dealId = data.get("dealId")
    assert utils.Is_uuid(dealId), f"{dealId} didn't match regex"

    # This can be extracted do different function
    endpoint = f"/api/v1/GetDeal/{dealId}"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data.get("expiresAt") == params.get("expiresAt")
    assert data.get("title") == params.get("title")
    assert data.get("description") == params.get("description")
    assert data.get("isVerified") == None
    assert data.get("verifiedAt") == None
    assert data.get("category") == None

    params = {
        "title": "New Title",
        "description": "New title desc",
        "expiresAt": "2030-12-31T23:59:59+00:00",
    }
    endpoint = f"/api/v1/UpdateDeal/{dealId}"
    response = requests.put(f"{BASE_URL}{endpoint}", headers=HEADERS, json=params)
    assert response.status_code == 204
    assert response.text == ""

    endpoint = f"/api/v1/GetDeal/{dealId}"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data.get("expiresAt") == params.get("expiresAt")
    assert data.get("title") == params.get("title")
    assert data.get("description") == params.get("description")

    endpoint = f"/api/v1/DeleteDeal/{dealId}"
    response = requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)
    assert response.status_code == 204
    assert response.text == ""

    endpoint = f"/api/v1/GetDeal/{dealId}"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)
    assert response.status_code == 404
    assert response.text == f"Deal with id '{dealId}' not found."


def test_verified_date_is_correct():
    endpoint = "/api/v1/CreateDeal"
    params = {
        "title": "Old Title",
        "description": "Old title desc",
        "domain": "example1.com",
        "code": "SAVE20",
        "expiresAt": "2025-12-31T23:59:59+00:00",
    }
    response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=params)
    print(response.text)
    assert response.status_code == 201
    data = response.json()
    dealId = data.get("dealId")
    print(dealId)

    endpoint = f"/api/v1/GetDeal/{dealId}"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)

    # Cleanup
    endpoint = f"/api/v1/DeleteDeal/{dealId}"
    requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)

    assert response.status_code == 200
    data = response.json()
    assert data.get("expiresAt") == params.get("expiresAt")
    assert data.get("title") == params.get("title")
    assert data.get("description") == params.get("description")
    assert data.get("category") == None
    assert data.get("isVerified") == None
    assert data.get("verifiedAt") == None


def test_post_verified_date_is_correct():
    endpoint = "/api/v1/CreateDeal"
    params = {
        "title": "Old Title",
        "description": "Old title desc",
        "domain": "example2.com",
        "code": "SAVE20",
        "expiresAt": "2025-12-31T23:59:59+00:00",
    }
    response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=params)
    print(response.text)
    assert response.status_code == 201
    data = response.json()
    dealId = data.get("dealId")
    print(dealId)

    endpoint = f"/api/v1/GetDeal/{dealId}"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)

    # Cleanup
    endpoint = f"/api/v1/DeleteDeal/{dealId}"
    requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)

    assert response.status_code == 200
    data = response.json()
    assert data.get("expiresAt") == params.get("expiresAt")
    assert data.get("title") == params.get("title")
    assert data.get("description") == params.get("description")
    assert data.get("category") == None
    assert data.get("isVerified") == None
    assert data.get("verifiedAt") == None


def test_put_verified_date_is_correct():
    endpoint = "/api/v1/CreateDeal"
    params = {
        "title": "Old Title",
        "description": "Old title desc",
        "domain": "example3.com",
        "code": "SAVE20",
        "expiresAt": "2025-12-31T23:59:59+00:00",
    }
    response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, json=params)
    print(response.text)
    assert response.status_code == 201
    data = response.json()
    dealId = data.get("dealId")
    print(dealId)

    new_params = {"title": "New Title", "description": "New Desc"}
    endpoint = f"/api/v1/UpdateDeal/{dealId}"
    response = requests.put(f"{BASE_URL}{endpoint}", headers=HEADERS, json=new_params)

    assert response.status_code == 204
    assert response.text == ""
    endpoint = f"/api/v1/GetDeal/{dealId}"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)

    # Cleanup
    endpoint = f"/api/v1/DeleteDeal/{dealId}"
    requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)

    assert response.status_code == 200
    data = response.json()

    assert data.get("expiresAt") == None
    assert data.get("title") == new_params.get("title")
    assert data.get("description") == new_params.get("description")
    assert data.get("category") == None
    assert data.get("isVerified") == None
    assert data.get("verifiedAt") == None


def test_get_deals_green():
    """Test GET request to fetch deals"""
    endpoint = "/api/v1/GetDeals/example.com"
    params = {"isVerified": "true", "category": "Sport"}

    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params)

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, (list, dict))
    assert data.get("count") == 0
    assert data.get("deals") == []


def test_get_deal_green():
    """Test GET request to fetch deal"""
    endpoint = "/api/v1/GetDeal/1b442cb336add37e8375070627efe751"
    params = {"isVerified": "true", "category": "Sport"}

    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params)

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, (list, dict))
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
    endpoint = f"/api/v1/UpdateDeal/{non_existing_id}"
    response = requests.put(f"{BASE_URL}{endpoint}", headers=HEADERS, json=params)

    assert response.status_code == 404
    assert response.text == f"Deal with id '{non_existing_id}' not found."


def test_delete_on_non_existing():
    non_existing_id = "00000000000000000000000000000000"
    endpoint = f"/api/v1/DeleteDeal/{non_existing_id}"
    response = requests.delete(f"{BASE_URL}{endpoint}", headers=HEADERS)

    assert response.status_code == 404
    assert response.text == f"Deal with id '{non_existing_id}' not found."


def test_merchants_green():
    endpoint = f"/api/v1/GetMerchants"
    response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS)

    assert response.status_code == 200

    data = response.json()

    assert data.get("count") == 8
    assert data.get("merchants") == MERCHANTS_ARRAY
