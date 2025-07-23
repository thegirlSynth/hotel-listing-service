from pydantic import BaseModel
from datetime import date
from typing import List


class HotelSearchRequest(BaseModel):
    query: str
    guests: int
    checkin: date
    checkout: date


class HotelSearchResult(BaseModel):
    hotel_id: int
    hotel_name: str
    city: str
    state: str
    lowest_price: float
    amenities: List[str]
    image_url: str
    star_rating: float
    views_count: int
    min_no_guests: int
    max_no_guests: int

