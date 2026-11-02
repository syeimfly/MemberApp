from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Reward(Base):
    __tablename__ = "rewards"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False, default="")
    points_cost: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
