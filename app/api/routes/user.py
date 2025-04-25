from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.auth.hash import hash_password
from app.auth.auth import create_access_token


router = APIRouter()


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token}     #Return access_token or new user details?

