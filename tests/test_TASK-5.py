import httpx
import os
import pytest

BASE_URL = os.environ.get('TEST_BASE_URL', 'http://localhost:8000')

def test_task_5_success():
    response = httpx.post(f'{BASE_URL}/suppliers', json={'name': 'Supplier1', 'contact': 'contact1@example.com'}, timeout=10)
    assert response.status_code in [200, 201]

def test_task_5_invalid():
    response = httpx.post(f'{BASE_URL}/suppliers', json={'name': ''}, timeout=10)
    assert response.status_code in [400, 422]