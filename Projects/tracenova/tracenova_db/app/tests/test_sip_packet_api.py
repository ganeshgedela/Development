# app/tests/test_sip_packet_api.py
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

base_url = "/sip-packet"

sip_packet_data = {
    "timestamp": datetime.utcnow().isoformat(),
    "source": "10.0.0.1",
    "destination": "10.0.0.2",
    "sip_instance": "instance-1",
    "from_user": "sip:alice@example.com",
    "from_tag": "tag1",
    "to_user": "sip:bob@example.com",
    "to_tag": "tag2",
    "call_id": "call-12345"
}

def test_create_sip_packet():
    response = client.post(f"{base_url}/", json=sip_packet_data)
    assert response.status_code == 200
    global created_packet
    created_packet = response.json()
    assert created_packet["call_id"] == sip_packet_data["call_id"]

def test_get_all_sip_packets():
    response = client.get(f"{base_url}/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_sip_packet_by_id():
    response = client.get(f"{base_url}/{created_packet['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created_packet["id"]

def test_get_sip_packet_by_call_id():
    response = client.get(f"{base_url}/search/call-id", params={"call_id": sip_packet_data["call_id"]})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_sip_packets_by_id_range():
    response = client.get(f"{base_url}/range/id", params={"start_id": created_packet['id'], "end_id": created_packet['id']})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_sip_packets_by_time_range():
    start = (datetime.utcnow() - timedelta(minutes=10)).isoformat()
    end = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    response = client.get(f"{base_url}/range/time", params={"start_time": start, "end_time": end})
    assert response.status_code == 200

def test_create_bulk_sip_packets():
    bulk_data = [
        {**sip_packet_data, "call_id": f"bulk-call-{i}"} for i in range(2)
    ]
    response = client.post(f"{base_url}/bulk", json=bulk_data)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_delete_sip_packet():
    response = client.delete(f"{base_url}/{created_packet['id']}")
    assert response.status_code == 200
