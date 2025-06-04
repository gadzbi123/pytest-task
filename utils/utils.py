import re
import uuid


def Is_uuid(s):
    return bool(re.fullmatch(r"[0-9a-fA-F]{32}", s))


def get_unique_test_data(prefix=""):
    """Helper function to generate unique test data"""
    unique_id = str(uuid.uuid4())[:8]
    print(f"regression-test-{prefix}{unique_id}.com")
    return {
        "title": f"Regression Test Deal {prefix}{unique_id}",
        "description": f"Testing v1 vs v2 consistency {prefix}{unique_id}",
        "domain": f"regression-test-{prefix}{unique_id}.com",
        "code": f"REGRESS{prefix}{unique_id}",
        "expiresAt": "2025-12-31T23:59:59+00:00",
    }
