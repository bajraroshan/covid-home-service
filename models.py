from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db 

# db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(255), nullable=False)
    vaccinated = db.Column(db.String(10), nullable=False)
    occupation = db.Column(db.String(255), nullable=False)
    credit_card_number = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)  # Optionally, change to Integer type
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

class SOSContact(db.Model):
    __tablename__ = 'sos_contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    relationship = db.Column(db.String(100), nullable=False)

class GroceryItem(db.Model):
    __tablename__ = 'grocery_items'
    
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # Optional field for image URL or path
    description = db.Column(db.String(500), nullable=True)  # Optional short description



class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    grocery_item_id = db.Column(db.Integer, db.ForeignKey('grocery_items.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Establish a relationship to GroceryItem
    grocery_item = db.relationship('GroceryItem', backref='cart_items')


class Medication(db.Model):
    __tablename__ = 'medications'
    
    medication_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    doses_per_day = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    times = db.Column(db.String(255), nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)  # Set nullable=False if this should always be present

class HomeServiceCategory(db.Model):
    __tablename__ = 'home_service_categories'
    
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    subcategories = db.relationship('HomeServiceSubCategory', backref='category', lazy=True)

class HomeServiceSubCategory(db.Model):
    __tablename__ = 'home_service_subcategories'
    
    subcategory_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('home_service_categories.category_id'), nullable=False)
    description = db.Column(db.String(255), nullable=True)