from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Member, Reward
from schemas import RewardOut
from security import current_member

from .router import router


@router.get("", response_model=list[RewardOut])
def list_rewards(_member: Member = Depends(current_member), db: Session = Depends(get_db)):
    return db.query(Reward).filter_by(active=True).order_by(Reward.points_cost).all()
