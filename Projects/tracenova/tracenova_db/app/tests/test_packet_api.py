# app/tests/test_packet_api.py
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

client = TestClient(app)


def test_create_packet():
    response = client.post("/packet/", json={
        "timestamp": datetime.utcnow().isoformat(),
        "source": "10.0.0.1",
        "destination": "10.0.0.2",
        "protocol": "ICMP",
        "payload": "Ping"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["source"] == "10.0.0.1"


def test_get_all_packets():
    response = client.get("/packet/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_bulk_packets():
    bulk_data = [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "source": f"10.0.0.{i}",
            "destination": "10.0.1.1",
            "protocol": "UDP",
            "payload": f"Payload {i}"
        } for i in range(2)
    ]
    response = client.post("/packet/bulk", json=bulk_data)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_single_packet():
    create_resp = client.post("/packet/", json={
        "timestamp": datetime.utcnow().isoformat(),
        "source": "10.0.0.9",
        "destination": "10.0.0.10",
        "protocol": "TCP",
        "payload": "Data"
    })
    pkt_id = create_resp.json()["id"]
    response = client.get(f"/packet/{pkt_id}")
    assert response.status_code == 200
    assert response.json()["id"] == pkt_id


def test_delete_packet():
    create_resp = client.post("/packet/", json={
        "timestamp": datetime.utcnow().isoformat(),
        "source": "10.0.0.5",
        "destination": "10.0.0.6",
        "protocol": "HTTP",
        "payload": "GET /index.html"
    })
    pkt_id = create_resp.json()["id"]
    delete_resp = client.delete(f"/packet/{pkt_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["id"] == pkt_id
