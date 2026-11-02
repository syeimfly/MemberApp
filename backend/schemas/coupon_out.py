from datetime import datetime

from pydantic import BaseModel, ConfigDict

from models import CouponStatus


class CouponOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    reward_name: str
    points_spent: int
    status: CouponStatus
    created_at: datetime
    redeemed_at: datetime | None
