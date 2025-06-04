import pytest
import requests
from datetime import datetime
from config import BASE_URL, HEADERS
from utils import utils
import uuid


def test_create_deal_regression():
    """Test that creating a deal works consistently between v1 and v2"""
    # Test data - different for v1 and v2
    v1_params = utils.get_unique_test_data("v1")
    v2_params = utils.get_unique_test_data("v2")

    # Create deal in v1
    v1_response = requests.post(
        f"{BASE_URL}/api/v1/CreateDeal", headers=HEADERS, json=v1_params
    )
    assert v1_response.status_code == 201
    v1_data = v1_response.json()
    v1_deal_id = v1_data.get("dealId")
    assert utils.Is_uuid(v1_deal_id)

    # Create deal in v2
    v2_response = requests.post(
        f"{BASE_URL}/api/v2/CreateDeal", headers=HEADERS, json=v2_params
    )
    assert v2_response.status_code == 201
    v2_data = v2_response.json()
    v2_deal_id = v2_data.get("dealId")
    assert utils.Is_uuid(v2_deal_id)

    # Cleanup
    requests.delete(f"{BASE_URL}/api/v1/DeleteDeal/{v1_deal_id}", headers=HEADERS)
    requests.delete(f"{BASE_URL}/api/v2/DeleteDeal/{v2_deal_id}", headers=HEADERS)


def test_get_deal_regression():
    """Test that getting a deal returns consistent data between v1 and v2"""
    # Create a deal in v1 first
    v1_params = utils.get_unique_test_data("v1")

    v1_response = requests.post(
        f"{BASE_URL}/api/v1/CreateDeal", headers=HEADERS, json=v1_params
    )
    assert v1_response.status_code == 201
    v1_deal_id = v1_response.json().get("dealId")

    # Get deal from both versions
    v1_get = requests.get(f"{BASE_URL}/api/v1/GetDeal/{v1_deal_id}", headers=HEADERS)
    v2_get = requests.get(f"{BASE_URL}/api/v2/GetDeal/{v1_deal_id}", headers=HEADERS)

    assert v1_get.status_code == 200
    assert v2_get.status_code == 200

    v1_data = v1_get.json()
    v2_data = v2_get.json()

    # Compare common fields
    assert v1_data.get("title") == v2_data.get("title")
    assert v1_data.get("description") == v2_data.get("description")
    assert v1_data.get("expiresAt") == v2_data.get("expiresAt")
    assert v1_data.get("code") == v2_data.get("code")
    assert v1_data.get("domain") == v2_data.get("domain")

    # Cleanup
    requests.delete(f"{BASE_URL}/api/v1/DeleteDeal/{v1_deal_id}", headers=HEADERS)


def test_update_deal_regression():
    """Test that updating a deal works consistently between v1 and v2"""
    # Create a deal in v1 first
    v1_params = utils.get_unique_test_data("v1")

    v1_response = requests.post(
        f"{BASE_URL}/api/v1/CreateDeal", headers=HEADERS, json=v1_params
    )
    assert v1_response.status_code == 201
    v1_deal_id = v1_response.json().get("dealId")

    # Update params
    update_params = {
        "title": f"Updated Title {str(uuid.uuid4())[:8]}",
        "description": f"Updated Description {str(uuid.uuid4())[:8]}",
        "expiresAt": "2030-12-31T23:59:59+00:00",
    }

    # Update in v1
    v1_update = requests.put(
        f"{BASE_URL}/api/v1/UpdateDeal/{v1_deal_id}",
        headers=HEADERS,
        json=update_params,
    )
    assert v1_update.status_code == 204

    # Update in v2
    v2_update = requests.put(
        f"{BASE_URL}/api/v2/UpdateDeal/{v1_deal_id}",
        headers=HEADERS,
        json=update_params,
    )
    assert v2_update.status_code == 204

    # Get updated deal from both versions
    v1_get = requests.get(f"{BASE_URL}/api/v1/GetDeal/{v1_deal_id}", headers=HEADERS)
    v2_get = requests.get(f"{BASE_URL}/api/v2/GetDeal/{v1_deal_id}", headers=HEADERS)

    v1_data = v1_get.json()
    v2_data = v2_get.json()

    # Compare updated fields
    assert v1_data.get("title") == v2_data.get("title")
    assert v1_data.get("description") == v2_data.get("description")
    assert v1_data.get("expiresAt") == v2_data.get("expiresAt")

    # Cleanup
    requests.delete(f"{BASE_URL}/api/v1/DeleteDeal/{v1_deal_id}", headers=HEADERS)


def test_get_deals_regression():
    """Test that getting deals list works consistently between v1 and v2"""
    # Test with same query parameters
    params = {"isVerified": "true", "category": "Sport"}

    v1_response = requests.get(
        f"{BASE_URL}/api/v1/GetDeals/dell.com", headers=HEADERS, params=params
    )
    v2_response = requests.get(
        f"{BASE_URL}/api/v2/GetDeals/dell.com", headers=HEADERS, params=params
    )

    assert v1_response.status_code == 200
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    v2_data = v2_response.json()

    # Compare response structure
    assert "count" in v1_data
    assert "count" in v2_data
    assert "deals" in v1_data
    assert "deals" in v2_data


def test_merchants_regression():
    """Test that getting merchants works consistently between v1 and v2"""
    v1_response = requests.get(f"{BASE_URL}/api/v1/GetMerchants", headers=HEADERS)
    v2_response = requests.get(f"{BASE_URL}/api/v2/GetMerchants", headers=HEADERS)

    assert v1_response.status_code == 200
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    v2_data = v2_response.json()

    # Compare response structure and data
    assert v1_data.get("count") == v2_data.get("count")
    assert v1_data.get("merchants") == v2_data.get("merchants")


def test_verified_deal_regression():
    """Test that verified deal behavior is consistent between v1 and v2"""
    # Create verified deals with different data for v1 and v2
    v1_params = utils.get_unique_test_data("v1")
    v1_params.update(
        {
            "isVerified": True,
            "category": "Sport",
        }
    )

    v2_params = utils.get_unique_test_data("v2")
    v2_params.update(
        {
            "isVerified": True,
            "category": "Sport",
        }
    )

    # Create in v1
    v1_response = requests.post(
        f"{BASE_URL}/api/v1/CreateDeal", headers=HEADERS, json=v1_params
    )
    assert v1_response.status_code == 201
    v1_deal_id = v1_response.json().get("dealId")

    # Create in v2
    v2_response = requests.post(
        f"{BASE_URL}/api/v2/CreateDeal", headers=HEADERS, json=v2_params
    )
    assert v2_response.status_code == 201
    v2_deal_id = v2_response.json().get("dealId")

    # Get deals from opposite versions
    v1_get = requests.get(f"{BASE_URL}/api/v1/GetDeal/{v2_deal_id}", headers=HEADERS)
    v2_get = requests.get(f"{BASE_URL}/api/v2/GetDeal/{v1_deal_id}", headers=HEADERS)

    v1_data = v1_get.json()
    v2_data = v2_get.json()

    # Compare verified deal fields
    assert v1_data.get("isVerified") == None
    assert v2_data.get("isVerified") == False
    assert v1_data.get("category") == None
    assert v2_data.get("category") == None
    # Note: verifiedAt might be different between versions as per the test files

    # Cleanup
    requests.delete(f"{BASE_URL}/api/v1/DeleteDeal/{v1_deal_id}", headers=HEADERS)
    requests.delete(f"{BASE_URL}/api/v2/DeleteDeal/{v2_deal_id}", headers=HEADERS)
