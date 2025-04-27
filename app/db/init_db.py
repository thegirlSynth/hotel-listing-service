from app.db.session import SessionLocal
from app.models.user import User, RoleEnum
from app.auth.hash import hash_password
from sqlalchemy.orm import Session


def init_superuser(db: Session):

    existing_user = db.query(User).filter(User.email == "owner@example.com").first()
    if not existing_user:
        owner = User(
            username= "default_owner",
            email="owner@example.com",
            hashed_password =hash_password("ownerpass123"),
            role = RoleEnum.owner
            )

        db.add(owner)
        db.commit()


def setup():
    db = SessionLocal()
    try:
        init_superuser(db)
        print("Superuser initialized!")
    finally:
        db.close()

if __name__ == "__main__":
    setup()
