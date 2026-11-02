from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from balance import get_balance
from database import get_db
from models import Member
from schemas import StaffMemberOut

from .router import router


@router.get("/{code}", response_model=StaffMemberOut)
def get_member(code: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter_by(code=code.strip().upper()).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return StaffMemberOut(code=member.code, name=member.name, balance=get_balance(db, member.id))
