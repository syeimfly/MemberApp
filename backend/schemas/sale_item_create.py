from pydantic import BaseModel, Field


class SaleItemCreate(BaseModel):
    product_id: int
    qty: int = Field(gt=0)
