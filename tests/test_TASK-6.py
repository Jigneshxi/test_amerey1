import httpx
import os
import pytest

BASE_URL = os.environ.get('TEST_BASE_URL', 'http://localhost:8000')

def test_task_6_success():
    response = httpx.post(f'{BASE_URL}/mappings', json={'supplier_field': 'field1', 'internal_field': 'field2'}, timeout=10)
    assert response.status_code in [200, 201]

def test_task_6_invalid():
    response = httpx.post(f'{BASE_URL}/mappings', json={'supplier_field': ''}, timeout=10)
    assert response.status_code in [400, 422]