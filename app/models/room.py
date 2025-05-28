from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"))
    room_type = Column(String)
    price_per_night = Column(Float)
    max_guests = Column(Integer)
    availability = Column(Boolean, default=True)

    hotel = relationship("Hotel", back_populates="rooms")
