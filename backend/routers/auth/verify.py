from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import LoginAttempt
from security import create_token

from .router import router


class VerifyRequest(BaseModel):
    nonce: str


@router.post("/verify")
def verify_login(body: VerifyRequest, response: Response, db: Session = Depends(get_db)):
    """The app polls this: 202 until the member presses Start in Telegram, then 200 with a JWT."""
    attempt = db.query(LoginAttempt).filter_by(nonce=body.nonce).first()
    now = datetime.now(timezone.utc)
    if attempt is None or attempt.used_at or attempt.expires_at.replace(tzinfo=timezone.utc) < now:
        raise HTTPException(status_code=400, detail="Login expired, start again")
    if attempt.member_id is None:
        response.status_code = 202
        return {"status": "pending"}
    attempt.used_at = now
    db.commit()
    return {"status": "ok", "token": create_token(attempt.member_id)}
