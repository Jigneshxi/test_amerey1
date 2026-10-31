import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_18_retailer_login_success():
    response = httpx.post(f"{BASE_URL}/retailer/login", json={'username': 'retailer1', 'password': 'password'}, timeout=10)
    assert response.status_code == 200

def test_task_18_browse_catalog_success():
    response = httpx.get(f"{BASE_URL}/retailer/products", headers={'Authorization': 'Bearer test_token'}, timeout=10)
    assert response.status_code == 200

def test_task_18_place_order_success():
    payload = {'product_id': '123', 'quantity': 10}
    response = httpx.post(f"{BASE_URL}/retailer/orders", json=payload, headers={'Authorization': 'Bearer test_token'}, timeout=10)
    assert response.status_code in [200, 201]