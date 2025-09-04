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
        "Ikeja", "Surulere", "Epe", "Badagry", "Ikorodu",
        "Victoria Island", "Yaba", "Lekki", "Ajah", "Maryland"
    ],
    "Abuja": [
        "Garki", "Wuse", "Asokoro", "Maitama", "Gwarinpa",
        "Kubwa", "Utako", "Jabi", "Lugbe", "Lokogoma"
    ],
    "Rivers": [
        "Port Harcourt", "Obio-Akpor", "Bonny", "Degema", "Eleme",
        "Okrika", "Oyigbo", "Ahoada", "Omoku", "Bori"
    ],
    "Imo": [
        "Owerri", "Orlu", "Okigwe", "Mbaitoli", "Oguta",
        "Mbaise", "Nkwerre", "Obowo", "Isiala Mbano", "Ohaji"
    ],
    "Enugu": [
        "Enugu", "Nsukka", "Awgu", "Oji River", "Udi",
        "Ngwo", "Emene", "Abakpa", "Nike", "Agbani"
    ],
    "Abia": [
        "Umuahia", "Aba", "Ohafia", "Arochukwu", "Isiala Ngwa",
        "Bende", "Ukwa", "Isuikwuato", "Ikwuano", "Osisioma"
    ],
    "Cross River": [
        "Calabar", "Ogoja", "Obudu", "Ikom", "Ugep",
        "Akamkpa", "Bekwarra", "Biase", "Yala", "Obanliku"
    ],
    "AkwaIbom": [
        "Uyo", "Eket", "Ikot Ekpene", "Oron", "Abak",
        "Etinan", "Ikot Abasi", "Essien Udim", "Ibesikpo", "Itu"
    ],
    "Plateau": [
        "Jos", "Barkin Ladi", "Riyom", "Pankshin", "Langtang",
        "Shendam", "Mangu", "Bokkos", "Wase", "Qua'an Pan"
    ],
    "Oyo": [
        "Ibadan", "Ogbomoso", "Oyo", "Iseyin", "Eruwa",
        "Saki", "Igboho", "Lalupon", "Fiditi", "Kishi"
    ],
    "Ogun": [
        "Abeokuta", "Sagamu", "Ijebu Ode", "Ilaro", "Ota",
        "Ijebu Igbo", "Owode", "Ayetoro", "Agbara", "Obada"
    ],
    "Delta": [
        "Warri", "Asaba", "Sapele", "Ughelli", "Oghara",
        "Ogwashi-Uku", "Agbor", "Kwale", "Burutu", "Abraka"
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
amenity_types = [
    "Free Wi-Fi",
    "Air Conditioning",
    "Flat-Screen TV",
    "Room Service",
    "Complimentary Breakfast",
    "Swimming Pool",
    "Fitness Center",
    "Spa & Wellness Center",
    "Mini Bar",
    "Laundry Service",
    "24-Hour Front Desk",
    "Parking",
    "Airport Shuttle",
    "Pet-Friendly Rooms",
    "In-Room Safe",
]

amenities = []
for name in amenity_types:
    amenity = Amenity(name=name)
    db.add(amenity)
    amenities.append(amenity)
db.commit()

# Add 30 hotels per state
hotels = []
for state in states_cities:
    for _ in range(30):
        hotel_name = f"{fake.last_name()} {random.choice(['Hotel', 'Resort', 'Suites', 'Lodgings', 'Hotels'])}"
        city = random.choice(states_cities[state])
        address = f"{fake.building_number()}, {fake.street_name()}, {city}, {state} State"
        description = generate_hotel_description(hotel_name, city)
        is_featured = random.choice([True, False])
        category = random.choice(["luxury", ""])
        image = random.choice(image_url)
        star_rating = random.randint(20, 50) / 10
        views_count = random.randint(10, 200)


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
            category=category,
            views_count=views_count,
            image=image,
            )
        #add random amenities
        hotel.amenities = random.sample(amenities, k=random.randint(3, 7))

        db.add(hotel)
        hotels.append(hotel)

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
