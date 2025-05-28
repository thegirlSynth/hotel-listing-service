# seed.py
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.booking import Booking
from datetime import date, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

# Clear existing data
db.query(Booking).delete()
db.query(Room).delete()
db.query(Hotel).delete()

# Add sample hotels
hotels = [
    Hotel(name="Eko Hotel", city="Lagos", tags=["wifi", "pool", "breakfast"]),
    Hotel(name="Lagos Continental", city="Lagos", tags=["spa", "sea view"]),
    Hotel(name="Transcorp Hilton", city="Abuja", tags=["conference", "pool"]),
]

db.add_all(hotels)
db.commit()

# Add rooms for each hotel
rooms = [
    Room(hotel_id=hotels[0].id, room_type="Standard", price_per_night=35000, max_guests=2),
    Room(hotel_id=hotels[0].id, room_type="Deluxe", price_per_night=45000, max_guests=3),
    Room(hotel_id=hotels[1].id, room_type="Sea View", price_per_night=50000, max_guests=2),
    Room(hotel_id=hotels[2].id, room_type="Executive", price_per_night=60000, max_guests=4),
]

db.add_all(rooms)
db.commit()

# Add some sample bookings (to test availability filtering)
today = date.today()
bookings = [
    Booking(room_id=rooms[0].id, check_in_date=today + timedelta(days=5), check_out_data=today + timedelta(days=7)),
    Booking(room_id=rooms[2].id, check_in_date=today + timedelta(days=3), check_out_data=today + timedelta(days=10)),
]

db.add_all(bookings)
db.commit()

db.close()

print("Sample data seeded successfully.")
