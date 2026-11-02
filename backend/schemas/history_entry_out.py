from datetime import datetime

from pydantic import BaseModel


class HistoryEntryOut(BaseModel):
    kind: str  # "earned" or "spent"
    label: str
    points: int  # signed: positive when earned, negative when spent
    created_at: datetime
