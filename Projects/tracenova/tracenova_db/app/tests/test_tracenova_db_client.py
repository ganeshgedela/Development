# test_tracenova_db_client.py
import pytest
import requests
from unittest.mock import patch
from app.routers.tracenova_db_client import TraceNovaDBClient
from datetime import datetime

@pytest.fixture
def client():
    return TraceNovaDBClient(base_url="http://localhost:8000")

@patch("requests.post")
def test_insert_packet(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"protocol": "SIP"}
    packet = {"timestamp": "2025-01-01T00:00:00", "source": "10.0.0.1", "destination": "10.0.0.2", "protocol": "SIP", "payload": "{}"}
    res = client.insert_packet(packet)
    assert res["protocol"] == "SIP"

@patch("requests.post")
def test_insert_bulk_packets(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"inserted": 2}
    packets = [{"timestamp": "2025-01-01T00:00:00", "source": "10.0.0.1", "destination": "10.0.0.2", "protocol": "SIP", "payload": "{}"}]*2
    res = client.insert_bulk_packets(packets)
    assert res["inserted"] == 2

@patch("requests.get")
def test_get_packets(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"protocol": "SIP", "payload": "{}"},
        {"protocol": "DIAMETER", "payload": "{}"}
    ]
    res = client.get_packets()
    assert len(res) == 2
    assert res[0]["protocol"] == "SIP"

@patch("requests.delete")
def test_delete_packet(mock_delete, client):
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {"status": "deleted"}
    res = client.delete_packet(1)
    assert res["status"] == "deleted"

@patch("requests.get")
def test_get_packets_by_id_range(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"id": 1, "protocol": "SIP"},
        {"id": 2, "protocol": "SIP"}
    ]
    res = client.get_packets_by_id_range(1, 2)
    assert len(res) == 2
    assert res[0]["id"] == 1

# --- SIP Packet Tests ---
@patch("requests.post")
def test_insert_sip_packet(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"protocol": "SIP"}
    packet = {"timestamp": "2025-01-01T00:00:00", "source": "10.0.0.1", "destination": "10.0.0.2", "protocol": "SIP", "payload": "{}"}
    res = client.insert_sip_packet(packet)
    assert res["protocol"] == "SIP"

@patch("requests.get")
def test_get_sip_packets_by_call_id(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"call_id": "abc123", "protocol": "SIP"}
    ]
    res = client.get_sip_packets_by_call_id("abc123")
    assert res[0]["call_id"] == "abc123"

# --- Trace File Tests ---
@patch("requests.post")
def test_insert_network_trace(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"trace_name": "trace1"}
    trace = {"trace_name": "trace1", "status": "uploaded"}
    res = client.insert_network_trace(trace)
    assert res["trace_name"] == "trace1"

@patch("requests.patch")
def test_update_trace_status(mock_patch, client):
    mock_patch.return_value.status_code = 200
    mock_patch.return_value.json.return_value = {"status": "parsed"}
    res = client.update_trace_status(1, "parsed")
    assert res["status"] == "parsed"

@patch("requests.delete")
def test_delete_trace(mock_delete, client):
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {"status": "deleted"}
    res = client.delete_trace(1)
    assert res["status"] == "deleted"
