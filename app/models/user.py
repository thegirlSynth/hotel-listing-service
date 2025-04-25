from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base
import enum

class RoleEnum(str, enum.Enum):
    owner = "owner"
    admin = "admin"
    staff = "staff"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
