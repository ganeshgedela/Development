# tracenova_db_client.py
import requests
from typing import List, Optional
from datetime import datetime

class TraceNovaDBClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    # --- Packet APIs ---
    def insert_packet(self, packet: dict) -> dict:
        url = f"{self.base_url}/packets"
        response = requests.post(url, json=packet)
        response.raise_for_status()
        return response.json()

    def insert_bulk_packets(self, packets: List[dict]) -> dict:
        url = f"{self.base_url}/packets/bulk"
        response = requests.post(url, json={"packets": packets})
        response.raise_for_status()
        return response.json()

    def get_packets(self, skip: int = 0, limit: int = 100) -> List[dict]:
        url = f"{self.base_url}/packets"
        response = requests.get(url, params={"skip": skip, "limit": limit})
        response.raise_for_status()
        return response.json()

    def get_packets_by_id_range(self, start_id: int, end_id: int) -> List[dict]:
        url = f"{self.base_url}/packets/range"
        response = requests.get(url, params={"start_id": start_id, "end_id": end_id})
        response.raise_for_status()
        return response.json()

    def delete_packet(self, packet_id: int) -> dict:
        url = f"{self.base_url}/packets/{packet_id}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()

    def search_packets(self,
                       start_id: Optional[int] = None,
                       end_id: Optional[int] = None,
                       start_time: Optional[datetime] = None,
                       end_time: Optional[datetime] = None,
                       source: Optional[str] = None,
                       destination: Optional[str] = None,
                       protocol: Optional[str] = None) -> List[dict]:
        params = {
            "start_id": start_id,
            "end_id": end_id,
            "start_time": start_time,
            "end_time": end_time,
            "source": source,
            "destination": destination,
            "protocol": protocol
        }
        clean_params = {k: v for k, v in params.items() if v is not None}
        url = f"{self.base_url}/packets/search"
        response = requests.get(url, params=clean_params)
        response.raise_for_status()
        return response.json()

    # --- SIP Packet APIs ---
    def insert_sip_packet(self, packet: dict) -> dict:
        url = f"{self.base_url}/sip"
        response = requests.post(url, json=packet)
        response.raise_for_status()
        return response.json()

    def insert_bulk_sip_packets(self, packets: List[dict]) -> List[dict]:
        url = f"{self.base_url}/sip/bulk"
        response = requests.post(url, json=packets)
        response.raise_for_status()
        return response.json()

    def get_sip_packets(self, skip: int = 0, limit: int = 100) -> List[dict]:
        url = f"{self.base_url}/sip"
        response = requests.get(url, params={"skip": skip, "limit": limit})
        response.raise_for_status()
        return response.json()

    def get_sip_packet_by_id(self, sip_id: int) -> dict:
        url = f"{self.base_url}/sip/{sip_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def delete_sip_packet(self, sip_id: int) -> dict:
        url = f"{self.base_url}/sip/{sip_id}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()

    def get_sip_packets_by_id_range(self, start_id: int, end_id: int) -> List[dict]:
        url = f"{self.base_url}/sip/range/id"
        response = requests.get(url, params={"start_id": start_id, "end_id": end_id})
        response.raise_for_status()
        return response.json()

    def get_sip_packets_by_time_range(self, start_time: datetime, end_time: datetime) -> List[dict]:
        url = f"{self.base_url}/sip/range/time"
        response = requests.get(url, params={"start_time": start_time, "end_time": end_time})
        response.raise_for_status()
        return response.json()

    def get_sip_packets_by_call_id(self, call_id: str) -> List[dict]:
        url = f"{self.base_url}/sip/search/call-id"
        response = requests.get(url, params={"call_id": call_id})
        response.raise_for_status()
        return response.json()

    # --- Network Trace APIs ---
    def insert_network_trace(self, trace: dict) -> dict:
        url = f"{self.base_url}/trace"
        response = requests.post(url, json=trace)
        response.raise_for_status()
        return response.json()

    def get_all_traces(self, skip: int = 0, limit: int = 100) -> List[dict]:
        url = f"{self.base_url}/trace"
        response = requests.get(url, params={"skip": skip, "limit": limit})
        response.raise_for_status()
        return response.json()

    def get_trace_by_id(self, trace_id: int) -> dict:
        url = f"{self.base_url}/trace/{trace_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def update_trace_status(self, trace_id: int, status: str) -> dict:
        url = f"{self.base_url}/trace/{trace_id}/status"
        response = requests.patch(url, params={"status": status})
        response.raise_for_status()
        return response.json()

    def delete_trace(self, trace_id: int) -> dict:
        url = f"{self.base_url}/trace/{trace_id}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()
