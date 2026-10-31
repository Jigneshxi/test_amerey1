import httpx
import os
import pytest

BASE_URL = os.environ.get('TEST_BASE_URL', 'http://localhost:8000')

def test_task_11_success():
    order_data = {"productId": "123", "quantity": 10}
    response = httpx.post(f'{BASE_URL}/orders', json=order_data, timeout=10)
    assert response.status_code == 201
    data = response.json()
    assert 'orderId' in data

def test_task_11_invalid_product():
    order_data = {"productId": "invalid", "quantity": 10}
    response = httpx.post(f'{BASE_URL}/orders', json=order_data, timeout=10)
    assert response.status_code == 400