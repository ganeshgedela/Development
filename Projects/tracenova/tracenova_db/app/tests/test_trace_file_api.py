# app/tests/test_trace_file_api.py
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

client = TestClient(app)


def test_create_trace_file():
    response = client.post("/trace-file/", json={
        "file_name": "log001.pcap",
        "status": "pending",
        "notes": "initial test file"
    })
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_all_trace_files():
    response = client.get("/trace-file/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_trace_file_status():
    create_resp = client.post("/trace-file/", json={
        "file_name": "log002.pcap",
        "status": "pending",
        "notes": "file to be updated"
    })
    trace_id = create_resp.json()["id"]
    update_resp = client.patch(f"/trace-file/{trace_id}/status", params={"status": "processed"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "processed"


def test_delete_trace_file():
    create_resp = client.post("/trace-file/", json={
        "file_name": "log003.pcap",
        "status": "pending"
    })
    trace_id = create_resp.json()["id"]
    delete_resp = client.delete(f"/trace-file/{trace_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["id"] == trace_id
