import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_2_success():
    response = httpx.post(f"{BASE_URL}/transform/product", json={"productId": "123", "name": "Test Product", "price": 10.0}, timeout=10)
    assert response.status_code == 200

def test_task_2_invalid_input():
    response = httpx.post(f"{BASE_URL}/transform/product", json={"name": "Test Product"}, timeout=10)
    assert response.status_code == 400