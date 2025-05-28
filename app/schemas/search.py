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
    lowest_price: float
    tags: List[str]

