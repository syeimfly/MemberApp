from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models import Coupon, Sale


def get_balance(db: Session, member_id: int) -> int:
    """Points earned minus points spent on coupons. Computed, never stored, so it cannot drift."""
    earned = db.scalar(
        select(func.coalesce(func.sum(Sale.points_awarded), 0)).where(Sale.member_id == member_id))
    spent = db.scalar(
        select(func.coalesce(func.sum(Coupon.points_spent), 0)).where(
            Coupon.member_id == member_id))
    return earned - spent
