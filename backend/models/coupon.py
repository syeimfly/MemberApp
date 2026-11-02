from datetime import datetime
import enum

from sqlalchemy import String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import Base


class CouponStatus(str, enum.Enum):
    ISSUED = "issued"
    REDEEMED = "redeemed"


class Coupon(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True, nullable=False)
    reward_id: Mapped[int] = mapped_column(ForeignKey("rewards.id"), nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    points_spent: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[CouponStatus] = mapped_column(
        Enum(CouponStatus), nullable=False, default=CouponStatus.ISSUED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    redeemed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    reward: Mapped["Reward"] = relationship()

    @property
    def reward_name(self) -> str:
        return self.reward.name
