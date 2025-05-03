from pydantic import BaseModel

class BasePacket(BaseModel):
    timestamp: str
    source: str
    destination: str
    protocol: str
    payload: str
