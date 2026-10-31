import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_16_get_product_success():
    response = httpx.get(f"{BASE_URL}/products/123", headers={'Authorization': 'Bearer test_token'}, timeout=10)
    assert response.status_code == 200

def test_task_16_create_product_success():
    payload = {"name": "Test Product", "price": 19.99}
    response = httpx.post(f"{BASE_URL}/products", json=payload, headers={'Authorization': 'Bearer test_token'}, timeout=10)
    assert response.status_code in [200, 201]

def test_task_16_unauthorized_access():
    response = httpx.get(f"{BASE_URL}/products/123", timeout=10)
    assert response.status_code == 401