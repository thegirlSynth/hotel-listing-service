from sqlalchemy import Column, Integer, String, ForeignKey, Table
from app.db.base import Base


class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


#Association table between hotel and amenities
hotel_amenities = Table(
    "hotel_amenities",
    Base.metadata,
    Column("hotel_id", Integer, ForeignKey("hotels.id"), primary_key=True),
    Column("amenity_id", Integer, ForeignKey("amenities.id"), primary_key=True),
)
