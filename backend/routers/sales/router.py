from fastapi import APIRouter, Depends

from security import require_staff

router = APIRouter(prefix="/sales", tags=["sales"], dependencies=[Depends(require_staff)])
