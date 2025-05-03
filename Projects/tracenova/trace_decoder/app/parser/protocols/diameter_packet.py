from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DiameterPacket(BaseModel):
    timestamp: datetime = Field(..., alias="timestamp")
    session_id: Optional[str] = None
    origin_host: Optional[str] = None
    origin_realm: Optional[str] = None
    destination_host: Optional[str] = None
    destination_realm: Optional[str] = None
    command_code: Optional[str] = None
    application_id: Optional[str] = None
    result_code: Optional[str] = None
