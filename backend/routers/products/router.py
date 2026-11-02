from fastapi import APIRouter, Depends

from security import require_staff

router = APIRouter(prefix="/products", tags=["products"], dependencies=[Depends(require_staff)])
