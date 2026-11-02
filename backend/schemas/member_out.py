from pydantic import BaseModel


class MemberOut(BaseModel):
    name: str
    code: str
    balance: int
