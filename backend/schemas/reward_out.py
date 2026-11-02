from pydantic import BaseModel, ConfigDict


class RewardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    points_cost: int
