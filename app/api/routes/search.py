from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db
from app.schemas.search import HotelSearchRequest, HotelSearchResult
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.booking import Booking
from sqlalchemy import and_, or_, not_, exists, func


router  = APIRouter()


@router.get("/search-hotels", response_model=list[HotelSearchResult])
def search_hotels(
    query: str = Query(...),
    guests: int = Query(...),
    checkin: str = Query(...),
    checkout: str = Query(...),
    db: Session = Depends(get_db),
):

    checkin_date = checkin
    checkout_date = checkout

    subquery = db.query(Booking.room_id).filter(
        and_(
            Booking.status == "confirmed",
            Booking.check_in_date < checkout_date,
            Booking.check_out_data > checkin_date
        )
    ).subquery()

    hotels = (
        db.query(Hotel.id.label("hotel_id"),
                 Hotel.name.label("hotel_name"),
                 Hotel.city,
                 func.min(Room.price_per_night).label("lowest_price"),
                 Hotel.tags)
        .join(Room, Hotel.id == Room.hotel_id)
        .filter(
            or_(
                Hotel.name.ilike(f"%{query}%"),
                Hotel.city.ilike(f"%{query}%"),
                Hotel.country.ilike(f"%{query}%"),
            ),
            Room.max_guests >= guests,
            ~Room.id.in_(subquery)
        )
        .group_by(Hotel.id)
        .limit(50)
        .all()
    )

    return [HotelSearchResult(**hotel._mapping) for hotel in hotels]
