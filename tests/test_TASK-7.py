import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_7_error_handling_success():
    response = httpx.post(f"{BASE_URL}/error_handling", json={}, timeout=10)
    assert response.status_code == 200

def test_task_7_error_handling_failure():
    response = httpx.post(f"{BASE_URL}/error_handling", json={}, timeout=10)
    assert response.status_code in [500, 502]