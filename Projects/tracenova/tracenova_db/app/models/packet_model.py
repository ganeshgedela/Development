# app/models/packet_model.py

from sqlalchemy import Column, Integer, String, DateTime
from app.database.engine import Base

class Packet(Base):
    __tablename__ = "packets"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    protocol = Column(String, nullable=False)
    payload = Column(String, nullable=False)
