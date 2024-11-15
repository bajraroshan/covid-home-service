from app import db, create_app
from models import User  # Import User from the models module
from datetime import datetime
from utilities import generate_password_hash

# Create the Flask app context
app = create_app()

# Seed data for users

# Seed data for users
users = [
    User(
        first_name="Roshan",
        last_name="Bajracharya",
        email="roshan@example.com",
        password_hash=generate_password_hash("admin123"),
        address="123 Main St, Cityville",
        mobile_number="1234567890",
        phone_number="0987654321",
        country="CountryA",
        language="Nepali",
        vaccinated="Yes",
        occupation="Engineer",
        credit_card_number="4111111111111111",
        expiry_date="12/25",
        cvv="123",
        created_at=datetime.utcnow(),
        is_active=True,
        is_verified=True
    ),
    User(
        first_name="Saurab",
        last_name="Kharel",
        email="saurab@example.com",
        password_hash=generate_password_hash("admin123"),
        address="456 Maple Ave, Townsville",
        mobile_number="2345678901",
        phone_number="1234567890",
        country="CountryB",
        language="Nepali",
        vaccinated="Yes",
        occupation="Designer",
        credit_card_number="5555555555554444",
        expiry_date="11/24",
        cvv="456",
        created_at=datetime.utcnow(),
        is_active=True,
        is_verified=False
    ),
    User(
        first_name="Bidur",
        last_name="Dhakal",
        email="bidur@example.com",
        password_hash=generate_password_hash("admin123"),
        address="789 Oak Rd, Villageton",
        mobile_number="3456789012",
        phone_number="2345678901",
        country="CountryC",
        language="French",
        vaccinated="No",
        occupation="Teacher",
        credit_card_number="4012888888881881",
        expiry_date="10/23",
        cvv="789",
        created_at=datetime.utcnow(),
        is_active=False,
        is_verified=True
    ),
    User(
        first_name="Tushar",
        last_name="Verma",
        email="tushar@example.com",
        password_hash=generate_password_hash("admin123"),
        address="101 Pine St, Hamlet",
        mobile_number="4567890123",
        phone_number="3456789012",
        country="CountryD",
        language="German",
        vaccinated="No",
        occupation="Doctor",
        credit_card_number="4222222222222",
        expiry_date="01/26",
        cvv="321",
        created_at=datetime.utcnow(),
        is_active=True,
        is_verified=False
    ),
    User(
        first_name="Lucio",
        last_name="Lee",
        email="lucio@example.com",
        password_hash=generate_password_hash("admin123"),
        address="202 Birch Ln, Borough",
        mobile_number="5678901234",
        phone_number="4567890123",
        country="CountryE",
        language="Italian",
        vaccinated="Yes",
        occupation="Lawyer",
        credit_card_number="378282246310005",
        expiry_date="09/25",
        cvv="654",
        created_at=datetime.utcnow(),
        is_active=False,
        is_verified=True
    ),
    User(
        first_name="Kanak",
        last_name="Kanak",
        email="kanak@example.com",
        password_hash=generate_password_hash("admin123"),
        address="202 Birch Ln, Borough",
        mobile_number="5678901234",
        phone_number="4567890123",
        country="CountryE",
        language="Italian",
        vaccinated="Yes",
        occupation="Lawyer",
        credit_card_number="378282246310005",
        expiry_date="09/25",
        cvv="654",
        created_at=datetime.utcnow(),
        is_active=False,
        is_verified=True
    )
]

# Add users to the database
with app.app_context():
    db.session.bulk_save_objects(users)
    db.session.commit()
    print("Seed data added for users.")
