from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from database import Base
from models import Member, Reward, Sale
from routers.me.create_coupon import create_coupon
from routers.me.get_history import get_history
from routers.me.get_me import get_me
from routers.rewards.list_rewards import list_rewards
from schemas import CouponCreate


@pytest.fixture(name="db")
def db_fixture():
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([Member(code="M1", name="Sok"),
                         Reward(name="Coffee", points_cost=50),
                         Reward(name="Hidden", points_cost=10, active=False)])
        session.commit()
        yield session


def test_redeem_spends_points_and_lists_history(db):
    member = db.query(Member).one()
    reward = db.query(Reward).filter_by(name="Coffee").one()
    # older than the coupon: SQLite now() has 1s resolution, which would tie
    earlier = datetime.now(timezone.utc) - timedelta(days=1)
    db.add(Sale(member_id=member.id, total=70, points_awarded=70, created_at=earlier))
    db.commit()
    assert get_me(member, db).balance == 70

    coupon = create_coupon(CouponCreate(reward_id=reward.id), member, db)
    assert coupon.status == "issued" and coupon.points_spent == 50
    assert get_me(member, db).balance == 20

    kinds = [(e.kind, e.points) for e in get_history(member, db)]
    assert kinds == [("spent", -50), ("earned", 70)]

    with pytest.raises(HTTPException) as exc:  # 20 points left, reward costs 50
        create_coupon(CouponCreate(reward_id=reward.id), member, db)
    assert exc.value.status_code == 409


def test_inactive_or_missing_reward_is_404(db):
    member = db.query(Member).one()
    hidden = db.query(Reward).filter_by(name="Hidden").one()
    for reward_id in (hidden.id, 999):
        with pytest.raises(HTTPException) as exc:
            create_coupon(CouponCreate(reward_id=reward_id), member, db)
        assert exc.value.status_code == 404


def test_rewards_list_hides_inactive(db):
    member = db.query(Member).one()
    assert [r.name for r in list_rewards(member, db)] == ["Coffee"]
