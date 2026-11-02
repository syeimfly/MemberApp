from fastapi import Depends
from sqlalchemy.orm import Session

from balance import get_balance
from database import get_db
from models import Member
from schemas import MemberOut
from security import current_member

from .router import router


@router.get("", response_model=MemberOut)
def get_me(member: Member = Depends(current_member), db: Session = Depends(get_db)):
    return MemberOut(name=member.name, code=member.code, balance=get_balance(db, member.id))
