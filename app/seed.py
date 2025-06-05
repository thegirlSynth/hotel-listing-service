from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.booking import Booking
from datetime import date, timedelta
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Create tables
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

# Clear existing data
db.query(Booking).delete()
db.query(Room).delete()
db.query(Hotel).delete()
db.commit()

# Sample tags
tag_pool = [
    "wifi", "pool", "breakfast", "spa", "gym", "sea view", "conference",
    "pet-friendly", "bar", "free parking", "restaurant", "airport shuttle",
    "family-friendly", "business center"
]
cities = ["Lagos", "Abuja"]
room_types = ["Standard", "Deluxe", "Executive", "Suite", "Penthouse"]

# Add 15 realistic hotels
hotels = []
for _ in range(15):
    hotel_name = f"{fake.last_name()} {random.choice(['Hotel', 'Resort', 'Suites', 'Inn'])}"
    city = random.choice(cities)
    tags = random.sample(tag_pool, k=random.randint(2, 5))

    hotel = Hotel(name=hotel_name, city=city, tags=tags)
    db.add(hotel)
    hotels.append(hotel)

db.commit()

# Add rooms to hotels
rooms = []
for hotel in hotels:
    num_rooms = random.randint(3, 7)
    for _ in range(num_rooms):
        room = Room(
            hotel_id=hotel.id,
            room_type=random.choice(room_types),
            price_per_night=random.randint(25000, 120000),
            max_guests=random.choice([1, 2, 3, 4, 5])
        )
        db.add(room)
        rooms.append(room)

db.commit()

# Add 30 bookings with varying lengths and overlap
today = date.today()
for _ in range(30):
    room = random.choice(rooms)
    check_in_offset = random.randint(1, 30)
    stay_length = random.randint(1, 7)
    booking = Booking(
        room_id=room.id,
        check_in_date=today + timedelta(days=check_in_offset),
        check_out_date=today + timedelta(days=check_in_offset + stay_length)
    )
    db.add(booking)

db.commit()
db.close()

print("Sample data seeded successfully.")
