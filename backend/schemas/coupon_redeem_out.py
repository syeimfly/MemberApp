from pydantic import BaseModel


class CouponRedeemOut(BaseModel):
    code: str
    reward_name: str
    member_name: str
