from sqlalchemy.orm import Session
from typing import Optional
from app.models.hotel_evaluation import HotelEvaluation, EvaluationCategory
from app.models.hotel import Hotel
from app.services.hotel_evaluation_rules import (
    evaluate_luxury,
    evaluate_budget,
    evaluate_featured,
    evaluate_editors_pick,
)


def _apply_editors_pick(hotel: Hotel, scores: dict) -> None:
    is_editors_pick, total = evaluate_editors_pick(scores)
    hotel.is_editors_pick = is_editors_pick
    hotel.editors_pick_total = total


CATEGORY_HANDLERS = {
    EvaluationCategory.LUXURY: lambda hotel, scores: setattr(hotel, "is_luxury", evaluate_luxury(scores)),
    EvaluationCategory.BUDGET: lambda hotel, scores: setattr(hotel, "is_budget", evaluate_budget(scores)),
    EvaluationCategory.FEATURED: lambda hotel, scores: setattr(hotel, "is_featured", evaluate_featured(scores)),
    EvaluationCategory.EDITORS_PICK: _apply_editors_pick,
}


def add_evaluation(
    db: Session,
    hotel: Hotel,
    category: EvaluationCategory,
    scores: dict,
    notes: Optional[str] = None,
) -> HotelEvaluation:
    """
    Add a new evaluation for a hotel and update its flags.
    """

    # Ensure category exclusivity for luxury/budget
    if category in (EvaluationCategory.LUXURY, EvaluationCategory.BUDGET):
        hotel.is_luxury = False
        hotel.is_budget = False

    # Apply handler if exists
    handler = CATEGORY_HANDLERS.get(category)
    if handler:
        handler(hotel, scores)

    # Create and persist evaluation
    new_eval = HotelEvaluation(
        hotel_id=hotel.id,
        category=category,
        scores=scores,
        notes=notes,
    )
    db.add(new_eval)
    db.commit()
    db.refresh(new_eval)

    return new_eval
