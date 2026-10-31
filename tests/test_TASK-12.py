import httpx
import os
import pytest

BASE_URL = os.environ.get('TEST_BASE_URL', 'http://localhost:8000')

def test_task_12_success():
    inventory_update = {"productId": "456", "quantity": 50}
    response = httpx.post(f'{BASE_URL}/inventory', json=inventory_update, timeout=10)
    assert response.status_code == 200

def test_task_12_conflict():
    inventory_update = {"productId": "456", "quantity": -10}
    response = httpx.post(f'{BASE_URL}/inventory', json=inventory_update, timeout=10)
    assert response.status_code == 409