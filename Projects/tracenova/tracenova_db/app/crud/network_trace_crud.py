from sqlalchemy.orm import Session
from app.models.network_trace_model import NetworkTraceFile
from app.schemas.network_trace_schema import NetworkTraceFileCreate

def create_trace_file(db: Session, trace: NetworkTraceFileCreate):
    db_file = NetworkTraceFile(**trace.model_dump())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_trace_file(db: Session, trace_id: int):
    return db.query(NetworkTraceFile).filter(NetworkTraceFile.id == trace_id).first()

def get_all_trace_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(NetworkTraceFile).offset(skip).limit(limit).all()

def update_trace_file_status(db: Session, trace_id: int, status: str):
    db_file = db.query(NetworkTraceFile).filter(NetworkTraceFile.id == trace_id).first()
    if db_file:
        db_file.status = status
        db.commit()
        db.refresh(db_file)
    return db_file

def delete_trace_file(db: Session, trace_id: int):
    db_file = db.query(NetworkTraceFile).filter(NetworkTraceFile.id == trace_id).first()
    if db_file:
        db.delete(db_file)
        db.commit()
    return db_file
