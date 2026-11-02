import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import telegram_bot
from database import get_db
from models import LoginAttempt

from .router import router

NONCE_MINUTES = 10


@router.post("/start")
def start_login(db: Session = Depends(get_db)):
    if not telegram_bot.username:
        raise HTTPException(status_code=503, detail="Telegram bot is not running")
    nonce = secrets.token_urlsafe(16)
    expires = datetime.now(timezone.utc) + timedelta(minutes=NONCE_MINUTES)
    db.add(LoginAttempt(nonce=nonce, expires_at=expires))
    db.commit()
    return {"nonce": nonce, "link": f"https://t.me/{telegram_bot.username}?start={nonce}"}
