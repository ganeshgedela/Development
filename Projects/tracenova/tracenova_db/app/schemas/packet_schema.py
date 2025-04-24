from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class PacketBase(BaseModel):
    timestamp: datetime = Field(..., alias="timestamp")
    source: str = Field(..., alias="source")
    destination: str = Field(..., alias="destination")
    protocol: str = Field(..., alias="protocol")
    payload: str = Field(..., alias="payload")

    class ConfigDict:
        from_attributes = True
        populate_by_name = True  # Accepts both alias and original names

class PacketCreate(PacketBase):
    pass

class PacketOut(PacketBase):
    id: int
    model_config = ConfigDict(from_attributes=True)