# app/routers/packet_routes.py

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from fastapi import Query
from app.database.engine import get_db
from datetime import datetime
from app.schemas.packet_schema import PacketCreate, PacketOut
from app.crud import packet_crud
from typing import List
from typing import Optional

router = APIRouter()

@router.post("/", response_model=PacketOut)
def create_packet(packet: PacketCreate, db: Session = Depends(get_db)):
    return packet_crud.create_packet(db, packet)

@router.post("/bulk", response_model=List[PacketOut])
def create_bulk_packets(packets: List[PacketCreate] = Body(...), db: Session = Depends(get_db)):
    return packet_crud.create_bulk_packets(db, packets)

@router.get("/", response_model=List[PacketOut])
def read_packets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return packet_crud.get_all_packets(db, skip=skip, limit=limit)

@router.get("/{packet_id}", response_model=PacketOut)
def read_packet(packet_id: int, db: Session = Depends(get_db)):
    pkt = packet_crud.get_packet(db, packet_id)
    if not pkt:
        raise HTTPException(status_code=404, detail="Packet not found")
    return pkt

@router.delete("/{packet_id}", response_model=PacketOut)
def delete_packet(packet_id: int, db: Session = Depends(get_db)):
    pkt = packet_crud.delete_packet(db, packet_id)
    if not pkt:
        raise HTTPException(status_code=404, detail="Packet not found")
    return pkt

@router.get("/search", response_model=List[PacketOut])
def search_packets(
    start_id: Optional[int] = Query(None),
    end_id: Optional[int] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    source: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    protocol: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return packet_crud.search_packets(
        db=db,
        start_id=start_id,
        end_id=end_id,
        start_time=start_time,
        end_time=end_time,
        source=source,
        destination=destination,
        protocol=protocol
    )