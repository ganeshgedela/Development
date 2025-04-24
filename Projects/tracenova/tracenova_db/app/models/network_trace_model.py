from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.engine import Base

class NetworkTraceFile(Base):
    __tablename__ = "network_trace_files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # optional: choices like 'pending', 'processed', 'failed'
    notes = Column(String, nullable=True)
