from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.models.user import User, RoleEnum
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.auth.auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = verify_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_role(required_role: RoleEnum):
    def role_checker(user: User = Depends(get_current_user)):
        # In this implementation, I've assumed this hierarchy: "Owner" > "Admin" > "Staff"
        role_hierarchy = {
            RoleEnum.owner: 4,
            RoleEnum.admin: 3,
            RoleEnum.staff: 2,
            RoleEnum.user: 1,
        }
        if role_hierarchy[user.role] < role_hierarchy[required_role]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
