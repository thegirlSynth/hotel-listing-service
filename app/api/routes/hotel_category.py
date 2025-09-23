from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db
from app.schemas.search import HotelSearchResponse
from app.services.hotel_search_service import perform_category_search
from app.services.redis_service import store_search_session


router = APIRouter()


@router.get("/editors-pick", response_model=HotelSearchResponse, description="Returns hotels tagged editor's pick")
def editors_pick(db: Session = Depends(get_db)):
    hotels, hotel_ids = perform_category_search(db, "editors")
    session_id = store_search_session(hotel_ids)
    return {"session_id": session_id, "results": hotels}


@router.get("/luxury-hotels", response_model=HotelSearchResponse, description="Returns hotels tagged luxury")
def luxury_hotels(db: Session = Depends(get_db)):
    hotels, hotel_ids = perform_category_search(db, "luxury")
    session_id = store_search_session(hotel_ids)
    return {"session_id": session_id, "results": hotels}


@router.get("/budget-hotels", response_model=HotelSearchResponse, description="Returns hotels tagged budget")
def budget_hotels(db: Session = Depends(get_db)):
    hotels, hotel_ids = perform_category_search(db, "budget")
    session_id = store_search_session(hotel_ids)
    return {"session_id": session_id, "results": hotels}


@router.get("/featured-hotels", response_model=HotelSearchResponse, description="Returns hotels tagged featured")
def featured_hotels(db: Session = Depends(get_db)):
    hotels, hotel_ids = perform_category_search(db, "featured")
    session_id = store_search_session(hotel_ids)
    return {"session_id": session_id, "results": hotels}
