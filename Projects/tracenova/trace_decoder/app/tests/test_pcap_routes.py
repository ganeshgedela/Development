import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from trace_decoder.app.main import app

client = TestClient(app)

@patch("trace_decoder.app.api.pcap_routes.parse_pcap_file")
@patch("trace_decoder.app.api.pcap_routes.tracenova_db_client.insert_bulk_packets")
def test_decode_pcap_success(mock_insert, mock_parse):
    # Mock parser output
    mock_parse.return_value = [{
        "timestamp": "2025-01-01T12:00:00",
        "source": "1.1.1.1",
        "destination": "2.2.2.2",
        "protocol": "SIP",
        "payload": "INVITE"
    }]
    # Mock DB insert (do nothing)
    mock_insert.return_value = None

    # Simulate file upload
    files = {"file": ("sample.pcap", b"dummy content", "application/octet-stream")}
    response = client.post("/decode/pcap/file", files=files)

    assert response.status_code == 200
    assert response.json()["packet_count"] == 1
    mock_parse.assert_called_once()
    mock_insert.assert_called_once()
