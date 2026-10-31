import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_19_success():
    response = httpx.post(f"{BASE_URL}/alerts/test", timeout=10)
    assert response.status_code == 200
    assert "alert triggered successfully" in response.text.lower()

def test_task_19_failure():
    response = httpx.post(f"{BASE_URL}/alerts/test?error=true", timeout=10)
    assert response.status_code == 500
    assert "error occurred" in response.text.lower()