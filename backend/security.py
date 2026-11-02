import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from models import Member

JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-me-in-production-0123456789")
TOKEN_DAYS = 30
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O/1/I, members read these aloud

bearer = HTTPBearer()


def new_code() -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(8))


def create_token(member_id: int) -> str:
    exp = datetime.now(timezone.utc) + timedelta(days=TOKEN_DAYS)
    return jwt.encode({"sub": str(member_id), "exp": exp}, JWT_SECRET, algorithm="HS256")


def current_member(
    creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)
) -> Member:
    try:
        member_id = int(jwt.decode(creds.credentials, JWT_SECRET, algorithms=["HS256"])["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc
    member = db.get(Member, member_id)
    if member is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return member


def require_staff(x_staff_key: str = Header(default="")) -> None:
    staff_key = os.environ.get("STAFF_KEY", "")
    if not staff_key:
        raise HTTPException(status_code=503, detail="STAFF_KEY is not configured")
    if not secrets.compare_digest(x_staff_key.encode(), staff_key.encode()):
        raise HTTPException(status_code=401, detail="Wrong staff key")
