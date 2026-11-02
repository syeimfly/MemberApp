from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from balance import get_balance
from database import get_db
from models import Coupon, Member, Reward
from schemas import CouponCreate, CouponOut
from security import current_member, new_code

from .router import router


@router.post("/coupons", response_model=CouponOut)
def create_coupon(
    body: CouponCreate, member: Member = Depends(current_member), db: Session = Depends(get_db)
):
    reward = db.get(Reward, body.reward_id)
    if reward is None or not reward.active:
        raise HTTPException(status_code=404, detail="Reward not found")
    # lock the member row so two concurrent redeems cannot both pass the balance check
    db.refresh(member, with_for_update=True)
    if get_balance(db, member.id) < reward.points_cost:
        raise HTTPException(status_code=409, detail="Not enough points")
    coupon = Coupon(member_id=member.id, reward_id=reward.id, code=new_code(),
                    points_spent=reward.points_cost)
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon
