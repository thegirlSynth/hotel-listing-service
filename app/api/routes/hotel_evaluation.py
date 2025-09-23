# Make this a protected route later on
# Ideally, this should be behind the admin hms, for when the field analyst uploads hotel scores and clicks apply/categorize

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db
from app.models.hotel import Hotel
from app.schemas.hotel_evaluation import HotelEvaluationCreate, HotelEvaluationResponse
from app.services.hotel_eval_service import add_evaluation


router = APIRouter()


@router.post(
    "/hotels/{hotel_id}/evaluations",
    response_model=HotelEvaluationResponse
)
def create_hotel_evaluation(
    hotel_id: int,
    evaluation: HotelEvaluationCreate,
    db: Session = Depends(get_db),
):
    hotel = db.query(Hotel).get(hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    new_eval = add_evaluation(
        db=db,
        hotel=hotel,
        category=evaluation.category,
        scores=evaluation.scores or {},
        notes=evaluation.notes,
    )
    return new_eval
