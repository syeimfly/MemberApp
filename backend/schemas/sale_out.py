from pydantic import BaseModel


class SaleOut(BaseModel):
    sale_id: int
    member_name: str
    total: float
    points_awarded: int
    balance: int
