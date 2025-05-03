from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime
from app.models.sip_packet_model import SipPacket
from app.schemas.sip_packet_schema import SipPacketCreate

def create_sip_packet(db: Session, sip: SipPacketCreate):
    db_sip = SipPacket(**sip.model_dump())
    db.add(db_sip)
    db.commit()
    db.refresh(db_sip)
    return db_sip

def get_sip_packets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SipPacket).offset(skip).limit(limit).all()

def get_sip_packet(db: Session, id: int):
    return db.query(SipPacket).filter(SipPacket.id == id).first()

def delete_sip_packet(db: Session, id: int):
    sip = db.query(SipPacket).filter(SipPacket.id == id).first()
    if sip:
        db.delete(sip)
        db.commit()
    return sip

def create_bulk_sip_packets(db: Session, packets: list[SipPacketCreate]):
    db_packets = [SipPacket(**pkt.model_dump()) for pkt in packets]
    db.add_all(db_packets)  # ensures IDs are generated properly
    db.commit()
    for packet in db_packets:
        db.refresh(packet)  # ensures we get auto-generated IDs
    return db_packets

def get_sip_packets_by_id_range(db: Session, start_id: int, end_id: int) -> List[SipPacket]:
    return db.query(SipPacket).filter(SipPacket.id >= start_id, SipPacket.id <= end_id).all()

def get_sip_packets_by_time_range(db: Session, start_time: datetime, end_time: datetime) -> List[SipPacket]:
    return db.query(SipPacket).filter(SipPacket.timestamp >= start_time, SipPacket.timestamp <= end_time).all()

def get_sip_packets_by_call_id(db: Session, call_id: str) -> List[SipPacket]:
    return db.query(SipPacket).filter(SipPacket.call_id == call_id).all()