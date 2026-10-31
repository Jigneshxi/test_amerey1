import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_13_success():
    response = httpx.get(f"{BASE_URL}/reports", timeout=10)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_task_13_invalid_date_range():
    response = httpx.get(f"{BASE_URL}/reports?start_date=invalid&end_date=invalid", timeout=10)
    assert response.status_code in [400, 422]