import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_20_success():
    response = httpx.post(f"{BASE_URL}/archive/test", timeout=10)
    assert response.status_code == 200
    assert "archived successfully" in response.text.lower()

def test_task_20_failure():
    response = httpx.post(f"{BASE_URL}/archive/test?error=true", timeout=10)
    assert response.status_code == 500
    assert "archiving failed" in response.text.lower()