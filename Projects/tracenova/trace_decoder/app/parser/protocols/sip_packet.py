from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SipPacket(BaseModel):
    timestamp: datetime = Field(..., alias="timestamp")
    call_id: Optional[str] = None
    cseq: Optional[str] = None
    from_tag: Optional[str] = None
    to_tag: Optional[str] = None
    sip_instance: Optional[str] = None
    method: Optional[str] = None
    via: Optional[str] = None
    p_asserted_identity: Optional[str] = None
    request_uri: Optional[str] = None
    user_agent: Optional[str] = None
    contact: Optional[str] = None
