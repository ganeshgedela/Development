# app/crud/packet_crud.py

from sqlalchemy.orm import Session
from app.models.packet_model import Packet
from app.schemas.packet_schema import PacketCreate
from typing import List
from datetime import datetime
from typing import Optional

# Create a new packet
def create_packet(db: Session, packet: PacketCreate):
    db_packet = Packet(**packet.model_dump())
    db.add(db_packet)
    db.commit()
    db.refresh(db_packet)
    return db_packet

# Bulk create packets
def create_bulk_packets(db: Session, packets: List[PacketCreate]):
    db_packets = []
    for pkt in packets:
        db_packet = Packet(**pkt.model_dump())
        db.add(db_packet)
        db_packets.append(db_packet)

    db.commit()  # 💡 Commit once after all adds
    for db_packet in db_packets:
        db.refresh(db_packet)  # ✅ Refresh to populate ID
    return db_packets


# Get a single packet by ID
def get_packet(db: Session, packet_id: int):
    return db.query(Packet).filter(Packet.id == packet_id).first()

# Get all packets (with pagination)
def get_all_packets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Packet).offset(skip).limit(limit).all()

# Delete a packet by ID
def delete_packet(db: Session, packet_id: int):
    pkt = db.query(Packet).filter(Packet.id == packet_id).first()
    if pkt:
        db.delete(pkt)
        db.commit()
    return pkt

def search_packets(
    db: Session,
    start_id: Optional[int] = None,
    end_id: Optional[int] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    source: Optional[str] = None,
    destination: Optional[str] = None,
    protocol: Optional[str] = None,
):
    query = db.query(Packet)
    
    if start_id is not None:
        query = query.filter(Packet.id >= start_id)
    if end_id is not None:
        query = query.filter(Packet.id <= end_id)
    if start_time is not None:
        query = query.filter(Packet.timestamp >= start_time)
    if end_time is not None:
        query = query.filter(Packet.timestamp <= end_time)
    if source:
        query = query.filter(Packet.source == source)
    if destination:
        query = query.filter(Packet.destination == destination)
    if protocol:
        query = query.filter(Packet.protocol == protocol)

    return query.all()