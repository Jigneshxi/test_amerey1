import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_15_access_denied():
    response = httpx.get(f"{BASE_URL}/data", headers={}, timeout=10)
    assert response.status_code == 401

def test_task_15_encrypted_data():
    response = httpx.get(f"{BASE_URL}/data", headers={}, timeout=10)
    assert response.status_code == 200
    # Basic check - ideally, verify the data format is encrypted.
    assert isinstance(response.json(), list)