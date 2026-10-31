import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_8_validation_success():
    response = httpx.post(f"{BASE_URL}/data_validation", json={
        "productId": "123",
        "name": "Test Product",
        "price": 10.99
    }, timeout=10)
    assert response.status_code == 200

def test_task_8_validation_failure():
    response = httpx.post(f"{BASE_URL}/data_validation", json={
        "name": "Test Product"
    }, timeout=10)
    assert response.status_code == 400