import httpx
import os
import pytest

BASE_URL = os.environ.get('TEST_BASE_URL', 'http://localhost:8000')

def test_task_4_success():
    response = httpx.post(f'{BASE_URL}/products/deduplicate', json={'product_ids': ['product1', 'product2'] }, timeout=10)
    assert response.status_code in [200, 201]

def test_task_4_invalid():
    response = httpx.post(f'{BASE_URL}/products/deduplicate', json={'product_ids': []}, timeout=10)
    assert response.status_code in [400, 422]