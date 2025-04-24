from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.network_trace_schema import NetworkTraceFileCreate, NetworkTraceFileOut
from app.crud import network_trace_crud
from app.database.engine import get_db

router = APIRouter()

@router.post("/", response_model=NetworkTraceFileOut)
def create(trace: NetworkTraceFileCreate, db: Session = Depends(get_db)):
    return network_trace_crud.create_trace_file(db, trace)

@router.get("/", response_model=List[NetworkTraceFileOut])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return network_trace_crud.get_all_trace_files(db, skip, limit)

@router.get("/{trace_id}", response_model=NetworkTraceFileOut)
def read(trace_id: int, db: Session = Depends(get_db)):
    trace = network_trace_crud.get_trace_file(db, trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace file not found")
    return trace

@router.patch("/{trace_id}/status", response_model=NetworkTraceFileOut)
def update_status(trace_id: int, status: str, db: Session = Depends(get_db)):
    trace = network_trace_crud.update_trace_file_status(db, trace_id, status)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace file not found")
    return trace

@router.delete("/{trace_id}", response_model=NetworkTraceFileOut)
def delete(trace_id: int, db: Session = Depends(get_db)):
    trace = network_trace_crud.delete_trace_file(db, trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace file not found")
    return trace
