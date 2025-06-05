from sqlalchemy import Column, Integer, Date, ForeignKey, String
from app.db.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    status = Column(String, default="confirmed")
