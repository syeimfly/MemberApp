"""Idempotent demo data: python seed.py"""
from database import Base, engine, SessionLocal
from models import Member, Product, Reward

PRODUCTS = [("Espresso", 2.50), ("Latte", 3.80), ("Croissant", 2.20), ("Sandwich", 5.90)]
REWARDS = [
    ("Free coffee", "Any espresso-based drink", 50),
    ("Free pastry", "Croissant or muffin", 80),
    ("$5 off", "Off any order over $10", 120),
]


def seed():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.query(Product).count() == 0:
            db.add_all(Product(name=n, price=p) for n, p in PRODUCTS)
        if db.query(Reward).count() == 0:
            db.add_all(Reward(name=n, description=d, points_cost=c) for n, d, c in REWARDS)
        if not db.query(Member).filter_by(code="DEMO0001").first():
            db.add(Member(code="DEMO0001", name="Demo Member"))
        db.commit()


if __name__ == "__main__":
    seed()
    print("seeded")
