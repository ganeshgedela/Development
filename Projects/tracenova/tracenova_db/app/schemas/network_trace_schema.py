from pydantic import BaseModel, ConfigDict # type: ignore
from datetime import datetime
from typing import Optional

class NetworkTraceFileBase(BaseModel):
    file_name: str
    status: Optional[str] = "pending"
    notes: Optional[str] = None

class NetworkTraceFileCreate(NetworkTraceFileBase):
    pass

class NetworkTraceFileOut(NetworkTraceFileBase):
    id: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
