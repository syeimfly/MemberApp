from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

import telegram_bot
from database import Base
from models import LoginAttempt, Member
from routers.auth.start import start_login
from routers.auth.verify import VerifyRequest, verify_login
from security import create_token, current_member


@pytest.fixture(name="db")
def db_fixture():
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def tg(text, chat_id=111):
    return {"update_id": 1, "message": {
        "text": text, "chat": {"id": chat_id}, "from": {"first_name": "Sok"}}}


def test_full_login_flow(db, monkeypatch):
    monkeypatch.setattr(telegram_bot, "username", "memberbot")
    out = start_login(db)
    nonce = out["nonce"]
    assert out["link"] == f"https://t.me/memberbot?start={nonce}"

    res = Response()
    assert verify_login(VerifyRequest(nonce=nonce), res, db) == {"status": "pending"}
    assert res.status_code == 202

    assert "logged in" in telegram_bot.handle_update(db, tg(f"/start {nonce}"))
    member = db.query(Member).one()
    assert member.telegram_chat_id == 111

    out = verify_login(VerifyRequest(nonce=nonce), Response(), db)
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=out["token"])
    assert current_member(creds, db).id == member.id

    with pytest.raises(HTTPException):  # nonce is single-use
        verify_login(VerifyRequest(nonce=nonce), Response(), db)


def test_returning_member_is_reused(db, monkeypatch):
    monkeypatch.setattr(telegram_bot, "username", "memberbot")
    for _ in range(2):
        telegram_bot.handle_update(db, tg(f"/start {start_login(db)['nonce']}"))
    assert db.query(Member).count() == 1


def test_expired_nonce_rejected(db):
    db.add(LoginAttempt(nonce="old", expires_at=datetime.now(timezone.utc) - timedelta(minutes=1)))
    db.commit()
    assert "expired" in telegram_bot.handle_update(db, tg("/start old"))
    with pytest.raises(HTTPException):
        verify_login(VerifyRequest(nonce="old"), Response(), db)


def test_bad_token_rejected(db):
    with pytest.raises(HTTPException):
        current_member(HTTPAuthorizationCredentials(scheme="Bearer", credentials="junk"), db)
    with pytest.raises(HTTPException):  # valid signature, member does not exist
        current_member(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=create_token(999)), db)
