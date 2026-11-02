from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models  # noqa: F401  # pylint: disable=unused-import
import telegram_bot
from routers.auth import router as auth_router
from routers.me import router as me_router
from routers.rewards import router as rewards_router
from routers.products import router as products_router
from routers.members import router as members_router
from routers.sales import router as sales_router
from routers.coupons import router as coupons_router

@asynccontextmanager
async def lifespan(_app):
    # models import above registers the tables on Base
    # shortcut: create_all instead of Alembic, fine for a demo; add migrations before a real deploy
    Base.metadata.create_all(engine)
    telegram_bot.start_polling()
    yield

app = FastAPI(title="MemberApp", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(me_router)
app.include_router(rewards_router)
app.include_router(products_router)
app.include_router(members_router)
app.include_router(sales_router)
app.include_router(coupons_router)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
