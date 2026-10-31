import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_14_create_role_success():
    response = httpx.post(f"{BASE_URL}/roles", json={"name": "administrator", "permissions": ["read", "write"]}, timeout=10)
    assert response.status_code == 201

def test_task_14_get_role_invalid():
    response = httpx.get(f"{BASE_URL}/roles/invalid", timeout=10)
    assert response.status_code == 404