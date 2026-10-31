import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_3_success():
    response = httpx.post(f"{BASE_URL}/enrich/product", json={"productId": "123", "name": "Test Product", "price": 10.0}, timeout=10)
    assert response.status_code == 200

def test_task_3_product_not_found():
    response = httpx.post(f"{BASE_URL}/enrich/product", json={"productId": "456", "name": "Test Product", "price": 10.0}, timeout=10)
    assert response.status_code == 404