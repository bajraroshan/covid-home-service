import random
from app import db, create_app
from models import GroceryItem

# Initialize the Flask app
app = create_app()

# Example data pools
categories = ["Fruits", "Vegetables", "Meat", "Dairy", "Grains", "Bakery", "Beverages", "Snacks", "Frozen"]
items = {
    "Fruits": ["Apple", "Banana", "Orange", "Grapes", "Pineapple", "Strawberries", "Mango", "Blueberries"],
    "Vegetables": ["Broccoli", "Carrots", "Spinach", "Potatoes", "Onions", "Tomatoes", "Garlic", "Cucumber"],
    "Meat": ["Chicken Breast", "Pork Chops", "Beef Steak", "Lamb Chops", "Fish Fillet", "Turkey"],
    "Dairy": ["Milk", "Cheese", "Butter", "Yogurt", "Cream", "Eggs"],
    "Grains": ["Rice", "Pasta", "Quinoa", "Oats", "Couscous", "Barley"],
    "Bakery": ["Bread", "Croissant", "Muffin", "Bagel", "Cake", "Donut"],
    "Beverages": ["Orange Juice", "Coffee", "Tea", "Soda", "Water", "Energy Drink"],
    "Snacks": ["Chips", "Popcorn", "Cookies", "Crackers", "Pretzels", "Candy"],
    "Frozen": ["Pizza", "Ice Cream", "Frozen Veggies", "Chicken Nuggets", "Fish Sticks", "Fries"]
}

descriptions = [
    "Fresh and organic.",
    "Locally sourced and delicious.",
    "Perfect for healthy meals.",
    "Packed with nutrients and flavor.",
    "High quality and great taste.",
    "Ideal for quick snacks or recipes.",
]

# Generate placeholder images
def generate_image_url(name):
    base_url = "https://via.placeholder.com/150?text="
    return f"{base_url}{name.replace(' ', '+')}"

def generate_dummy_data(num_items=120):
    """Generate dummy grocery items."""
    groceries = []
    for _ in range(num_items):
        category = random.choice(categories)
        name = random.choice(items[category])
        price = round(random.uniform(0.5, 20.0), 2)  # Random price between $0.50 and $20
        quantity = random.randint(10, 500)  # Random quantity between 10 and 500
        description = random.choice(descriptions)
        image_url = generate_image_url(name)

        groceries.append(
            GroceryItem(
                name=name,
                category=category,
                price=price,
                quantity=quantity,
                description=description,
                image_url=image_url,
            )
        )
    return groceries

# Add to database
with app.app_context():
    try:
        # Clear existing data if needed
        GroceryItem.query.delete()
        db.session.commit()

        # Generate and add dummy data
        dummy_groceries = generate_dummy_data()
        db.session.bulk_save_objects(dummy_groceries)
        db.session.commit()
        print(f"{len(dummy_groceries)} grocery items added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")

