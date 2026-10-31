import httpx
import os
import pytest

BASE_URL = os.environ.get('TEST_BASE_URL', 'http://localhost:8000')

def test_task_10_success():
    response = httpx.get(f'{BASE_URL}/products', timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_task_10_invalid_auth():
    response = httpx.get(f'{BASE_URL}/products', headers={'Authorization': 'InvalidToken'}, timeout=10)
    assert response.status_code == 401