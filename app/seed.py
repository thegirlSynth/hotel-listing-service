from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.amenity import Amenity
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
db.query(Amenity).delete()
db.commit()


def generate_hotel_description(hotel_name, city):
    return (
        f"{hotel_name} offers {fake.catch_phrase().lower()} with "
        f"{fake.word()}-class service. Located in {city}, "
        f"guests enjoy {fake.bs()} and luxurious surroundings."
    )

states_cities = {
    "Lagos": [
        "Ikeja", "Epe", "Badagry", "Ikorodu",
        "Victoria Island", "Yaba", "Lekki", "Maryland"
    ],
    "Rivers": [
        "Port Harcourt"
    ],
    "Imo": [
        "Owerri"
    ],
    "Enugu": [
        "Enugu"
    ]
}


image_url = [
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058205/H1_vmojsx.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058205/H14_lr6pgj.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058206/H4_vhxcqx.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058206/H13_e9p6tl.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058207/H7_wygd3x.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058207/H15_uzxelu.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058207/H3_b4zh2b.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058208/H6_zitpae.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058208/H8_p7h7uo.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058209/H10_ntvmfk.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058209/H11_xh1xhw.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058209/H9_olpsih.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058210/H5_ypojv1.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058210/H12_fcwajb.png",
    "https://res.cloudinary.com/dvwqt9duj/image/upload/v1753058210/H2_hupwrd.png"
    ]

#Add amenities to DB
premium_amenity_types = [
    "Pool",
    "Gym/Fitness Center",
    "Spa/Wellness Center",
    "Fine Dining",
    "Rooftop Lounge/Bar",
    "Concierge Service",
    "Laundry/Butler Service",
    "Private Lounge/Executive Floor",
    "Valet Parking",
    "Conference/Event Hall",
    "In-Room Entertainment System",
    "Private Balcony/View Rooms"
]

budget_amenity_types = [
    "Free Wi-Fi",
    "Air Conditioning/Fan",
    "Clean Bathroom",
    "Comfortable Bed",
    "Secure Entry",
    "Low Noise Level",
    "Basic Room Cleaning",
    "TV/Entertainment Option",
    "Free Parking",
    "24/7 Front Desk/Contact "
]

premium_amenities = []
for name in premium_amenity_types:
    amenity = Amenity(name=name)
    db.add(amenity)
    premium_amenities.append(amenity)
db.commit()

budget_amenities = []
for name in budget_amenity_types:
    amenity = Amenity(name=name)
    db.add(amenity)
    budget_amenities.append(amenity)
db.commit()

# Add 30 hotels per state_city
hotels = []
for state in states_cities:
    for _ in range(30):
        hotel_name = f"{fake.last_name()} {random.choice(['Hotel', 'Resort', 'Suites', 'Lodgings', 'Hotels'])}"
        city = random.choice(states_cities[state])
        address = f"{fake.building_number()}, {fake.street_name()}, {city}, {state} State"
        description = generate_hotel_description(hotel_name, city)
        is_featured = random.choice([True, False])
        is_editors_pick = random.choice([True, False])
        is_budget = random.choice([True, False])
        is_luxury = not is_budget
        image = random.choice(image_url)
        star_rating = random.randint(20, 50) / 10
        views_count = random.randint(10, 200)
        amenities = (random.sample(premium_amenities, k=random.randint(1, 12))
                           + random.sample(budget_amenities, k=random.randint(1, 10)))


        hotel = Hotel(
            name=hotel_name,
            description=description,
            address=address,
            area=city,
            city=city,
            state=state,
            country="Nigeria",
            star_rating=star_rating,
            is_featured=is_featured,
            is_budget=is_budget,
            is_luxury=is_luxury,
            is_editors_pick=is_editors_pick,
            views_count=views_count,
            image=image,
            amenities=amenities
            )

        hotels.append(hotel)

db.add_all(hotels)
db.commit()

# Add rooms to hotels
room_types = ["Standard", "Deluxe", "Executive", "Suite", "Penthouse"]

rooms = []
for hotel in hotels:
    num_rooms = random.randint(3, 7)
    for _ in range(num_rooms):
        room = Room(
            hotel_id=hotel.id,
            room_type=random.choice(room_types),
            price_per_night=random.randint(25000, 120000),
            max_guests=random.choice([1, 2, 3, 4, 5, 6])
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
