from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Coupon, Member, Sale
from schemas import HistoryEntryOut
from security import current_member

from .router import router


@router.get("/history", response_model=list[HistoryEntryOut])
def get_history(member: Member = Depends(current_member), db: Session = Depends(get_db)):
    sales = db.query(Sale).filter_by(member_id=member.id).all()
    coupons = db.query(Coupon).filter_by(member_id=member.id).all()
    entries = [HistoryEntryOut(kind="earned", label="Purchase", points=s.points_awarded,
                               created_at=s.created_at) for s in sales]
    entries += [HistoryEntryOut(kind="spent", label=c.reward_name, points=-c.points_spent,
                                created_at=c.created_at) for c in coupons]
    return sorted(entries, key=lambda e: e.created_at, reverse=True)
