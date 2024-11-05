# Import necessary modules and models from your Flask app
from app import db, GroceryItem, app

# Dummy data for grocery items
dummy_groceries = [
    GroceryItem(name="Apple", category="Fruits", price=1.2, quantity=100),
    GroceryItem(name="Banana", category="Fruits", price=0.5, quantity=150),
    GroceryItem(name="Broccoli", category="Vegetables", price=1.0, quantity=75),
    GroceryItem(name="Chicken Breast", category="Meat", price=5.5, quantity=50),
    GroceryItem(name="Milk", category="Dairy", price=1.5, quantity=200),
    GroceryItem(name="Eggs", category="Dairy", price=3.0, quantity=60),
    GroceryItem(name="Rice", category="Grains", price=0.8, quantity=300),
    GroceryItem(name="Bread", category="Bakery", price=2.5, quantity=120),
    GroceryItem(name="Orange Juice", category="Beverages", price=3.0, quantity=80),
    GroceryItem(name="Pasta", category="Grains", price=1.2, quantity=200),
]

# Add dummy data to the database
with app.app_context():
    db.session.bulk_save_objects(dummy_groceries)
    db.session.commit()
    print("Dummy grocery data added successfully!")
