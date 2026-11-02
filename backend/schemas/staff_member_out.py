from pydantic import BaseModel


class StaffMemberOut(BaseModel):
    code: str
    name: str
    balance: int
