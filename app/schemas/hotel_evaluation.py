from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.hotel_evaluation import EvaluationCategory


class HotelEvaluationBase(BaseModel):
    category: EvaluationCategory
    scores: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class HotelEvaluationCreate(HotelEvaluationBase):
    pass


class HotelEvaluationUpdate(BaseModel):
    scores: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class HotelEvaluationInDBBase(HotelEvaluationBase):
    id: int
    hotel_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class HotelEvaluationResponse(HotelEvaluationInDBBase):
    pass
