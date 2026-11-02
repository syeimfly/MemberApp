from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Coupon, Member
from schemas import CouponOut
from security import current_member

from .router import router


@router.get("/coupons", response_model=list[CouponOut])
def list_coupons(member: Member = Depends(current_member), db: Session = Depends(get_db)):
    return db.query(Coupon).filter_by(member_id=member.id).order_by(Coupon.created_at.desc()).all()
