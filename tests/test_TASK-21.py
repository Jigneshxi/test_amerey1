import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_21_success():
    response = httpx.post(f"{BASE_URL}/edi/process", data="valid edi data", timeout=10)
    assert response.status_code == 200
    assert "edi processed successfully" in response.text.lower()

def test_task_21_failure():
    response = httpx.post(f"{BASE_URL}/edi/process", data="invalid edi data", timeout=10)
    assert response.status_code == 400
    assert "edi processing failed" in response.text.lower()