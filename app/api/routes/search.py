from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db
from app.schemas.search import HotelSearchResponse, HotelSearchResult
from app.services.hotel_search_service import perform_full_search, filter_cached_hotels
from app.services.redis_service import store_search_session


router = APIRouter()


@router.get("/search-hotels", response_model=HotelSearchResponse)
def search_hotels(
    query: str = Query(...),
    guests: int = Query(...),
    checkin: str = Query(...),
    checkout: str = Query(...),
    db: Session = Depends(get_db),
):
    hotels, hotel_ids = perform_full_search(db, query, guests, checkin, checkout)
    session_id = store_search_session(hotel_ids)
    return {"session_id": session_id, "results": hotels}


@router.get("/filter-hotels", response_model=list[HotelSearchResult])
def filter_hotels(
    session_id: str = Query(...),
    minprice: int = Query(None),
    maxprice: int = Query(None),
    amenities: str = Query(None),
    area: str = Query(None),
    rating: int = Query(None),
    db: Session = Depends(get_db),
):
    hotels = filter_cached_hotels(db, session_id, minprice, maxprice, amenities, area, rating)
    return hotels
