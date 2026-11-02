from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Product
from schemas import ProductOut

from .router import router


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).filter_by(active=True).order_by(Product.name).all()
