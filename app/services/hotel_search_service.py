from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_, or_, distinct
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.amenity import Amenity, hotel_amenities
from app.models.booking import Booking
from app.schemas.search import HotelSearchResult
from sqlalchemy.sql import select
from app.services.redis_service import get_cached_hotel_ids


def perform_full_search(db: Session, query, guests, checkin, checkout):
    # Build your base query here (same as before)
    subquery = select(Booking.room_id).where(
        and_(
            Booking.status == "confirmed",
            Booking.check_in_date < checkout,
            Booking.check_out_date > checkin
        )
    ).scalar_subquery()

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
        .join(hotel_amenities, Hotel.id == hotel_amenities.c.hotel_id)
        .join(Amenity, Amenity.id == hotel_amenities.c.amenity_id)
        .filter(
            or_(
                Hotel.name.ilike(f"%{query}%"),
                Hotel.city.ilike(f"%{query}%"),
                Hotel.state.ilike(f"%{query}%"),
                Hotel.country.ilike(f"%{query}%"),
            ),
            Room.max_guests >= guests,
            ~Room.id.in_(subquery)
        )
        .group_by(
            Hotel.id, Hotel.name, Hotel.city, Hotel.image,
            Hotel.star_rating, Hotel.views_count
        )
        .limit(50)
        .all()
    )

    hotel_ids = [h.hotel_id for h in hotels]
    return [HotelSearchResult(**hotel._mapping) for hotel in hotels], hotel_ids


def filter_cached_hotels(db: Session, session_id, minprice=None, maxprice=None, amenities=None, area=None, rating=None):
    hotel_ids = get_cached_hotel_ids(session_id)
    if not hotel_ids:
        return []

    query = db.query(
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
    ).join(Room, Hotel.id == Room.hotel_id
    ).join(hotel_amenities, Hotel.id == hotel_amenities.c.hotel_id
    ).join(Amenity, Amenity.id == hotel_amenities.c.amenity_id
    ).filter(Hotel.id.in_(hotel_ids))

    if minprice is not None:
        query = query.filter(Room.price_per_night >= minprice)
    if maxprice is not None:
        query = query.filter(Room.price_per_night <= maxprice)

    if area is not None:
        query = query.filter(Hotel.area.ilike(f"%{area}%"))

    if rating is not None:
        query = query.filter(
            and_(
                Hotel.star_rating >= rating,
                Hotel.star_rating < rating + 1  # Less than next whole number
                )
            )

    amenity_list = [a.strip().lower() for a in amenities.split(",")] if amenities else []
    if amenity_list:
        matched_hotels_subq = (
            db.query(hotel_amenities.c.hotel_id)
            .join(Amenity, Amenity.id == hotel_amenities.c.amenity_id)
            .filter(func.lower(Amenity.name).in_(amenity_list))
            .group_by(hotel_amenities.c.hotel_id)
            .having(func.count(distinct(Amenity.name)) == len(amenity_list))
            .subquery()
        )
        query = query.filter(Hotel.id.in_(select(matched_hotels_subq.c.hotel_id)))

    hotels = query.group_by(
        Hotel.id, Hotel.name, Hotel.city, Hotel.image,
        Hotel.star_rating, Hotel.views_count
    ).limit(50).all()

    return [HotelSearchResult(**hotel._mapping) for hotel in hotels]
