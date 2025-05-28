from sqlalchemy import Column, Integer, Date, ForeignKey, String
from app.db.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))
    check_in_date = Column(Date)
    check_out_data = Column(Date) #fix typo here and seed.py, search.py
    status = Column(String, default="confirmed")
