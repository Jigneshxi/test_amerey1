import httpx
import os
import pytest

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8000")

def test_task_23_success():
    rule_data = {"name": "Price Increase", "condition": {"field": "price", "operator": "gt", "value": 100}, "transformation": {"field": "price", "operation": "multiply", "value": 1.1}}
    response = httpx.post(f"{BASE_URL}/rules", json=rule_data, timeout=10)
    assert response.status_code == 201

def test_task_23_invalid_rule():
    rule_data = {"name": "Invalid Rule", "condition": {"field": "invalid_field"}}
    response = httpx.post(f"{BASE_URL}/rules", json=rule_data, timeout=10)
    assert response.status_code == 400