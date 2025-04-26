from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, get_current_user
from app.models.user import User, RoleEnum
from app.schemas.user import UserOut, RoleUpdateRequest
from app.auth.dependencies import require_role

router = APIRouter()

@router.patch("/users/{user_id}/role", response_model=UserOut)
def update_user_role(
    user_id: int,
    new_role: RoleUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != RoleEnum.owner:
        raise HTTPException(status_code=403, detail="Not authorized to update user roles.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.role = new_role.role
    db.commit()
    db.refresh(user)

    return user

@router.get("/protected")
def protected_route(user: User = Depends(get_current_user)):
    """
    Protected endpoint example
    """
    return {"message": f"Hello {user.username}, your role is {user.role.value}"}


@router.get("/admin-only")
def admin_only_route(user: User = Depends(require_role(RoleEnum.admin))):
    """
    Sample endpoint for actions that require Admin or higher
    """
    return {"message": f"Hello {user.username}, you have admin rights!"}

@router.get("/owner-only")
def owner_only_route(user: User = Depends(require_role(RoleEnum.owner))):
    """
    Sample endpoint for actions that require Owner
    """
    return {"message": f"Hello {user.username}, you have owner rights!"}
