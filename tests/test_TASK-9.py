import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_9_create_product_success():
    response = httpx.post(f"{BASE_URL}/products", json={
        "productId": "456",
        "name": "New Product",
        "price": 25.50
    }, timeout=10)
    assert response.status_code == 201

def test_task_9_get_product_success():
    response = httpx.get(f"{BASE_URL}/products/456", timeout=10)
    assert response.status_code == 200