from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db
from app.schemas.search import HotelSearchResponse, HotelSearchResult
from app.services.hotel_search_service import perform_full_search, filter_cached_hotels, return_all
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


@router.get("/filter-hotels", response_model=list[HotelSearchResult], description="This is the endpoint for performing any kind of hotel filtering, from all categories including all stays, editor's pick, luxury, bugget etc.")
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


@router.get("/all-stays", response_model=HotelSearchResponse, description="This returns all the hotels in the database.")
def all_stays(db: Session = Depends(get_db)):
    hotels, hotel_ids = return_all(db)
    session_id = store_search_session(hotel_ids)
    return {"session_id": session_id, "results": hotels}
