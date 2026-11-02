import os
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from balance import get_balance
from database import get_db
from models import Member, Product, Sale, SaleItem
from schemas import SaleCreate, SaleOut

from .router import router

POINTS_PER_UNIT = Decimal(os.environ.get("POINTS_PER_UNIT", "1"))
CENT = Decimal("0.01")


@router.post("", response_model=SaleOut)
def create_sale(body: SaleCreate, db: Session = Depends(get_db)):
    if not body.items:
        raise HTTPException(status_code=400, detail="Sale has no items")
    member = db.query(Member).filter_by(code=body.member_code.strip().upper()).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    sale = Sale(member_id=member.id, total=0, points_awarded=0)
    total = Decimal(0)
    for line in body.items:
        product = db.get(Product, line.product_id)
        if product is None or not product.active:
            raise HTTPException(status_code=404, detail=f"Product {line.product_id} not found")
        # str() first: price may arrive as float on some drivers
        unit_price = Decimal(str(product.price)).quantize(CENT, ROUND_HALF_UP)
        line_total = unit_price * line.qty
        total += line_total
        sale.items.append(SaleItem(product_id=product.id, qty=line.qty,
                                   unit_price=unit_price, line_total=line_total))
    sale.total = total
    sale.points_awarded = int((total * POINTS_PER_UNIT).to_integral_value(ROUND_DOWN))
    db.add(sale)
    db.commit()
    return SaleOut(sale_id=sale.id, member_name=member.name, total=float(total),
                   points_awarded=sale.points_awarded, balance=get_balance(db, member.id))
