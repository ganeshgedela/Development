# app/schemas/sip_packet_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class SipPacketBase(BaseModel):
    timestamp: datetime = Field(..., alias="timestamp")
    sip_instance: Optional[str] = Field(None, alias="sip_instance")
    from_user: str = Field(..., alias="from")
    from_tag: str = Field(..., alias="from_tag")
    to_user: str = Field(..., alias="to")
    to_tag: str = Field(..., alias="to_tag")
    call_id: str = Field(..., alias="call_id")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class SipPacketCreate(SipPacketBase):
    pass


class SipPacketOut(SipPacketBase):
    id: int = Field(..., alias="id")

