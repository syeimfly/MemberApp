from datetime import datetime, timezone

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Coupon, CouponStatus, Member
from schemas import CouponRedeemOut

from .router import router


@router.post("/{code}/redeem", response_model=CouponRedeemOut)
def redeem_coupon(code: str, db: Session = Depends(get_db)):
    # lock the row so a double scan cannot redeem the same coupon twice
    coupon = db.query(Coupon).filter_by(code=code.strip().upper()).with_for_update().first()
    if coupon is None:
        raise HTTPException(status_code=404, detail="Coupon not found")
    if coupon.status == CouponStatus.REDEEMED:
        raise HTTPException(status_code=409, detail="Coupon already used")
    coupon.status = CouponStatus.REDEEMED
    coupon.redeemed_at = datetime.now(timezone.utc)
    db.commit()
    member = db.get(Member, coupon.member_id)
    return CouponRedeemOut(
        code=coupon.code, reward_name=coupon.reward_name, member_name=member.name)
