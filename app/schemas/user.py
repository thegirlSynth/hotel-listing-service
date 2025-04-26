from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    owner = "owner"
    admin = "admin"
    staff = "staff"
    user = "user"

class RoleUpdateRequest(BaseModel):
    role: RoleEnum

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True
