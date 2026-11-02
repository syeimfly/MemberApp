from fastapi import APIRouter, Depends

from security import require_staff

router = APIRouter(prefix="/coupons", tags=["coupons"], dependencies=[Depends(require_staff)])
