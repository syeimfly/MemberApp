from pydantic import BaseModel


class CouponCreate(BaseModel):
    reward_id: int
