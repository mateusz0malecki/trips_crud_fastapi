from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    user_id: int
    name: str
    email: str
    password: str
    is_active: bool = True
    is_admin: bool = False


class ShowUser(BaseModel):
    name: str
    email: str
    is_active: bool = True
    is_admin: bool = False

    class Config:
        orm_mode = True


class EditUser(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class Trip(BaseModel):
    name: str
    email: str
    description: str
    completeness: bool = False
    contact: bool = False

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] | None = None
