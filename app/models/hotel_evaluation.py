from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, JSON, func, Enum as SqlEnum
from app.db.base import Base
from sqlalchemy.orm import relationship
from enum import Enum


class EvaluationCategory(str, Enum):
    LUXURY = "luxury"
    BUDGET = "budget"
    FEATURED = "featured"
    EDITORS_PICK = "editors_pick"


class HotelEvaluation(Base):
    __tablename__ = "hotel_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False)
    category = Column(SqlEnum(EvaluationCategory), index=True, nullable=False)
    scores = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    hotel = relationship("Hotel", back_populates="hotel_evaluations")
