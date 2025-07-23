from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db
from app.models.amenity import Amenity, hotel_amenities
from app.schemas.search import HotelSearchResult
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.booking import Booking
from sqlalchemy import and_, or_, func, select, distinct
from datetime import date

router  = APIRouter()


@router.get("/search-hotels", response_model=list[HotelSearchResult])
def search_hotels(
    query: str = Query(...),
    guests: int = Query(...),
    checkin: date = Query(...),
    checkout: date = Query(...),
    minprice: int = Query(None),
    maxprice: int = Query(None),
    area: str = Query(None),
    rating: float = Query(None),
    amenities: str = Query(None),  # comma-separated amenity names
    db: Session = Depends(get_db),
):

    amenity_list = [a.strip().lower() for a in amenities.split(",")] if amenities else []

    subquery = select(Booking.room_id).where(
        and_(
            Booking.status == "confirmed",
            Booking.check_in_date < checkout,
            Booking.check_out_date > checkin
        )
    ).scalar_subquery()

    filters = [
        or_(
            Hotel.name.ilike(f"%{query}%"),
            Hotel.city.ilike(f"%{query}%"),
            Hotel.state.ilike(f"%{query}%"),
            Hotel.country.ilike(f"%{query}%"),
        ),
        Room.max_guests >= guests,
        ~Room.id.in_(subquery),
    ]

    if minprice is not None:
        filters.append(Room.price_per_night >= minprice)
    if maxprice is not None:
        filters.append(Room.price_per_night <= maxprice)

    if area:
        filters.append(Hotel.area.ilike(f"%{area}%"))

    if rating:
        filters.append(Hotel.star_rating == rating)  #round up or down


    hotels = (
        db.query(
            Hotel.id.label("hotel_id"),
            Hotel.name.label("hotel_name"),
            Hotel.city,
            Hotel.state,
            Hotel.image.label("image_url"),
            Hotel.star_rating,
            Hotel.views_count,
            func.min(Room.price_per_night).label("lowest_price"),
            func.min(Room.max_guests).label("min_no_guests"),
            func.max(Room.max_guests).label("max_no_guests"),
            func.array_agg(distinct(Amenity.name)).label("amenities")
            )
        .join(Room, Hotel.id == Room.hotel_id)
        .join(hotel_amenities, Hotel.id == hotel_amenities.c.hotel_id)  # Join through the association table
        .join(Amenity, Amenity.id == hotel_amenities.c.amenity_id)
        .filter(*filters)
    )

    if amenity_list:
        print(amenity_list)
        matched_hotels_subq = (
            db.query(hotel_amenities.c.hotel_id)
            .join(Amenity, Amenity.id == hotel_amenities.c.amenity_id)
            .filter(func.lower(Amenity.name).in_(amenity_list))
            .group_by(hotel_amenities.c.hotel_id)
            .having(func.count(distinct(Amenity.name)) == len(amenity_list))
            .subquery()
        )

        hotels = hotels.filter(Hotel.id.in_(select(matched_hotels_subq.c.hotel_id)))


    hotels = hotels.group_by(
            Hotel.id, Hotel.name, Hotel.city, Hotel.image,
            Hotel.star_rating, Hotel.views_count
    ).limit(50).all()    #Work on pagination later


    return [HotelSearchResult(**hotel._mapping) for hotel in hotels]
