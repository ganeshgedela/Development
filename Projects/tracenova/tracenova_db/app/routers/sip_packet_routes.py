from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.schemas.sip_packet_schema import SipPacketCreate, SipPacketOut
from app.crud import sip_packet_crud
from app.database.engine import get_db

router = APIRouter()

@router.post("/", response_model=SipPacketOut)
def create_sip(sip: SipPacketCreate, db: Session = Depends(get_db)):
    return sip_packet_crud.create_sip_packet(db, sip)

@router.get("/", response_model=List[SipPacketOut])
def read_sip_packets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return sip_packet_crud.get_sip_packets(db, skip, limit)

@router.get("/{id}", response_model=SipPacketOut)
def read_sip_packet(id: int, db: Session = Depends(get_db)):
    sip = sip_packet_crud.get_sip_packet(db, id)
    if not sip:
        raise HTTPException(status_code=404, detail="SIP Packet not found")
    return sip

@router.delete("/{id}", response_model=SipPacketOut)
def delete_sip_packet(id: int, db: Session = Depends(get_db)):
    sip = sip_packet_crud.get_sip_packet(db, id)
    if not sip:
        raise HTTPException(status_code=404, detail="SIP Packet not found")
    return sip_packet_crud.delete_sip_packet(db, id)

@router.post("/bulk", response_model=List[SipPacketOut])
def create_bulk(packets: List[SipPacketCreate] = Body(...), db: Session = Depends(get_db)):
    return sip_packet_crud.create_bulk_sip_packets(db, packets)

@router.get("/range/id", response_model=List[SipPacketOut])
def get_packets_by_id_range(start_id: int = Query(...), end_id: int = Query(...), db: Session = Depends(get_db)):
    return sip_packet_crud.get_sip_packets_by_id_range(db, start_id, end_id)

@router.get("/range/time", response_model=List[SipPacketOut])
def get_packets_by_time_range(start_time: datetime = Query(...), end_time: datetime = Query(...), db: Session = Depends(get_db)):
    return sip_packet_crud.get_sip_packets_by_time_range(db, start_time, end_time)

@router.get("/search/call-id", response_model=List[SipPacketOut])
def get_packets_by_call_id(call_id: str = Query(...), db: Session = Depends(get_db)):
    return sip_packet_crud.get_sip_packets_by_call_id(db, call_id)