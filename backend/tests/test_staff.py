from datetime import datetime, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from database import Base
from models import Coupon, CouponStatus, Member, Product, Reward
from routers.coupons.redeem_coupon import redeem_coupon
from routers.members.get_member import get_member
from routers.products.list_products import list_products
from routers.sales import create_sale as create_sale_module
from routers.sales.create_sale import create_sale
from schemas import SaleCreate, SaleItemCreate
from security import require_staff


@pytest.fixture(name="db")
def db_fixture():
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([Member(code="ABC12345", name="Sok"),
                         Product(name="Latte", price=3.80),
                         Product(name="Muffin", price=2.25),
                         Product(name="Old", price=1, active=False),
                         Reward(name="Coffee", points_cost=50)])
        session.commit()
        yield session


def products(db):
    return {p.name: p.id for p in db.query(Product).all()}


def test_sale_totals_and_points_floor(db):
    ids = products(db)
    body = SaleCreate(member_code=" abc12345 ", items=[
        SaleItemCreate(product_id=ids["Latte"], qty=3),
        SaleItemCreate(product_id=ids["Muffin"], qty=1)])
    out = create_sale(body, db)
    assert out.total == 13.65  # 3 x 3.80 + 2.25, no float drift
    assert out.points_awarded == 13  # floor, not round
    assert out.balance == 13
    assert get_member("ABC12345", db).balance == 13


def test_points_per_unit_scales(db, monkeypatch):
    monkeypatch.setattr(create_sale_module, "POINTS_PER_UNIT", create_sale_module.Decimal("2"))
    body = SaleCreate(member_code="ABC12345",
                      items=[SaleItemCreate(product_id=products(db)["Latte"], qty=1)])
    assert create_sale(body, db).points_awarded == 7  # floor(3.80 x 2)


def test_bad_sales_rejected(db):
    ids = products(db)
    cases = [("ABC12345", [], 400), ("NOPE", [SaleItemCreate(product_id=ids["Latte"], qty=1)], 404),
             ("ABC12345", [SaleItemCreate(product_id=999, qty=1)], 404),
             ("ABC12345", [SaleItemCreate(product_id=ids["Old"], qty=1)], 404)]
    for code, items, status in cases:
        with pytest.raises(HTTPException) as exc:
            create_sale(SaleCreate(member_code=code, items=items), db)
        assert exc.value.status_code == status
    with pytest.raises(ValueError):  # qty must be positive
        SaleItemCreate(product_id=1, qty=0)


def test_product_list_hides_inactive(db):
    assert sorted(p.name for p in list_products(db)) == ["Latte", "Muffin"]


def test_coupon_is_single_use(db):
    member = db.query(Member).one()
    reward = db.query(Reward).one()
    db.add(Coupon(member_id=member.id, reward_id=reward.id, code="CPN00001", points_spent=50,
                  created_at=datetime.now(timezone.utc)))
    db.commit()
    out = redeem_coupon("cpn00001", db)
    assert (out.reward_name, out.member_name) == ("Coffee", "Sok")
    assert db.query(Coupon).one().status == CouponStatus.REDEEMED
    for code, status in (("CPN00001", 409), ("NOPE", 404)):
        with pytest.raises(HTTPException) as exc:
            redeem_coupon(code, db)
        assert exc.value.status_code == status


def test_staff_key_check(monkeypatch):
    monkeypatch.setenv("STAFF_KEY", "secret")
    require_staff("secret")
    for bad, status in (("wrong", 401), ("", 401)):
        with pytest.raises(HTTPException) as exc:
            require_staff(bad)
        assert exc.value.status_code == status
    monkeypatch.setenv("STAFF_KEY", "")
    with pytest.raises(HTTPException) as exc:
        require_staff("")
    assert exc.value.status_code == 503
