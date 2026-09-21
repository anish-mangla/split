from pydantic import BaseModel


class CreateGroupRequest(BaseModel):
    name: str


class AddMemberRequest(BaseModel):
    user_id: int

class LoginRequest(BaseModel):
    email: str
    password: str