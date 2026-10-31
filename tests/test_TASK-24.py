import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_24_success():
    product_id = "123"
    # First create a product
    initial_data = {"productId": product_id, "name": "Test Product", "price": 100}
    response = httpx.post(f"{BASE_URL}/products", json=initial_data, timeout=10)
    assert response.status_code == 201

    # Then update the product
    update_data = {"name": "Updated Product", "price": 120}
    response = httpx.put(f"{BASE_URL}/products/{product_id}", json=update_data, timeout=10)
    assert response.status_code == 200

    # Get the versions
    version_response = httpx.get(f"{BASE_URL}/products/{product_id}/versions", timeout=10)
    assert version_response.status_code == 200
    versions = version_response.json()
    assert len(versions) == 2


def test_task_24_invalid_id():
    response = httpx.get(f"{BASE_URL}/products/invalid_id/versions", timeout=10)
    assert response.status_code == 404