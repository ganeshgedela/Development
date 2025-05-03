# app/models/sip_packet_model.py
from sqlalchemy import Column, Integer, String, DateTime
from app.database.engine import Base
from datetime import datetime

class SipPacket(Base):
    __tablename__ = "sip_packets"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sip_instance = Column(String(255), nullable=True)     # length added
    from_user = Column(String(128), nullable=False)
    from_tag = Column(String(128), nullable=False)
    to_user = Column(String(128), nullable=False)
    to_tag = Column(String(128), nullable=False)
    call_id = Column(String(255), nullable=False)
