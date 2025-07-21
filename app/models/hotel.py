from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DateTime
from app.models.amenity import hotel_amenities
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    address = Column(String)
    area = Column(String)
    city = Column(String, index=True)
    state = Column(String)
    country = Column(String)
    star_rating = Column(Integer)
    is_featured = Column(Boolean, default=False)
    category = Column(String)
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    rooms = relationship("Room", back_populates="hotel", cascade="all, delete")

    amenities = relationship("Amenity", secondary=hotel_amenities, backref="hotels")
