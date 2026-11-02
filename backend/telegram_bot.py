"""Telegram login bot: long polling, no public URL. Swap to a webhook at deploy time."""
import json
import os
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from database import SessionLocal
from models import LoginAttempt, Member
from security import new_code

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"
username = ""  # pylint: disable=invalid-name  # filled by getMe when polling starts


def _call(method: str, **params):
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(f"{API}/{method}", data, timeout=40) as resp:
        return json.load(resp)["result"]


def handle_update(db: Session, update: dict) -> str | None:
    """Link the sender's chat to the login attempt in `/start <nonce>`. Returns the reply text."""
    msg = update.get("message") or {}
    parts = (msg.get("text") or "").split()
    if not parts or parts[0] != "/start":
        return None
    if len(parts) < 2:
        return "Open the MemberApp login page and tap the Telegram button to sign in."
    attempt = db.query(LoginAttempt).filter_by(nonce=parts[1]).first()
    now = datetime.now(timezone.utc)
    if attempt is None or attempt.used_at or attempt.expires_at.replace(tzinfo=timezone.utc) < now:
        return "This login link has expired. Go back to the app and try again."
    chat_id = msg["chat"]["id"]
    member = db.query(Member).filter_by(telegram_chat_id=chat_id).first()
    if member is None:
        name = (msg.get("from") or {}).get("first_name") or "Member"
        member = Member(code=new_code(), name=name, telegram_chat_id=chat_id)
        db.add(member)
        db.flush()
    attempt.member_id = member.id
    db.commit()
    return f"Hi {member.name}, you're logged in. Head back to the app."


def _poll():
    global username  # pylint: disable=global-statement
    username = _call("getMe")["username"]
    offset = 0
    while True:
        try:
            for update in _call("getUpdates", offset=offset, timeout=30):
                offset = update["update_id"] + 1
                with SessionLocal() as db:
                    reply = handle_update(db, update)
                if reply:
                    _call("sendMessage", chat_id=update["message"]["chat"]["id"], text=reply)
        except Exception as exc:  # pylint: disable=broad-except  # keep the bot alive on network/db errors
            print(f"telegram poll error: {exc}")
            time.sleep(5)


def start_polling():
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN not set, login bot disabled")
        return
    threading.Thread(target=_poll, daemon=True).start()
