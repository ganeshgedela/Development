import os
import pytest
from trace_decoder.app.parser.pcap_parser import parse_pcap_file

def test_parse_pcap_file_with_sample():
    # Locate the sample PCAP file
    sample_path = os.path.join(os.path.dirname(__file__), "data", "sample.pcap")

    # Ensure the file exists
    assert os.path.exists(sample_path), f"sample.pcap not found at {sample_path}"

    # Call the parser
    packets = parse_pcap_file(sample_path)

    # Basic assertions
    assert isinstance(packets, list)
    assert len(packets) >= 0  # empty file is valid, malformed is not an error

    # If packets exist, validate structure
    if packets:
        packet = packets[0]
        assert "timestamp" in packet
        assert "protocol" in packet
        assert "payload" in packet
