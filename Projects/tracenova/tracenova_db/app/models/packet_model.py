# app/models/packet_model.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import JSON
from app.database.engine import Base

class Packet(Base):
    __tablename__ = "packets"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    source = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    protocol = Column(String(50), nullable=False)
    payload = Column(JSON, nullable=False)
