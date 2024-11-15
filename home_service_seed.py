from app1 import HomeServiceCategory, HomeServiceSubCategory, db, app

def seed_data():
    with app.app_context():
        # Disable autoflush to prevent premature database writes during checks
        with db.session.no_autoflush:
            print("Seeding Home Service Categories...")

            # Categories
            categories = {
                "Cleaning Service": None,
                "Plumbing Service": None,
                "Electrical Service": None,
                "Appliance Service": None,
                "Home Improvement Service": None,
                "Pest Control Service": None,
                "Gardening and Landscaping Service": None
            }

            # Check if categories exist; if not, create them
            for name in categories.keys():
                category = HomeServiceCategory.query.filter_by(name=name).first()
                if not category:
                    category = HomeServiceCategory(name=name)
                    db.session.add(category)
                categories[name] = category

            db.session.flush()  # Ensure IDs are assigned to categories before adding subcategories

            # Subcategories for each category
            subcategories = [
                # Cleaning Service Subcategories
                ("Regular House Cleaning", "Thorough, everyday cleaning.", categories["Cleaning Service"]),
                ("Deep Cleaning", "In-depth cleaning for hard-to-reach areas.", categories["Cleaning Service"]),
                ("Carpet Cleaning", "Carpet washing and stain removal.", categories["Cleaning Service"]),
                ("Window Cleaning", "Streak-free window cleaning.", categories["Cleaning Service"]),

                # Plumbing Service Subcategories
                ("Leak Repair", "Quick fixes for leaking pipes.", categories["Plumbing Service"]),
                ("Drain Unclogging", "Efficient drain clearing service.", categories["Plumbing Service"]),
                ("Pipe Installation", "Installation of new pipes.", categories["Plumbing Service"]),

                # Electrical Service Subcategories
                ("Light Installation", "Professional light installation service.", categories["Electrical Service"]),
                ("Electrical Wiring", "Safe and reliable wiring.", categories["Electrical Service"]),
                ("Appliance Installation", "Installation for home appliances.", categories["Electrical Service"]),

                # Appliance Service Subcategories
                ("Air Conditioner", "AC installation and maintenance.", categories["Appliance Service"]),
                ("Washing Machine", "Washing machine setup and repair.", categories["Appliance Service"]),
                ("Refrigerator", "Fridge installation and repair.", categories["Appliance Service"]),
                ("Microwave/Oven", "Microwave and oven installation.", categories["Appliance Service"]),

                # Home Improvement Subcategories
                ("Flooring", "Professional flooring services.", categories["Home Improvement Service"]),
                ("Painting", "Interior and exterior painting.", categories["Home Improvement Service"]),
                ("Handyman", "General handyman services.", categories["Home Improvement Service"]),

                # Pest Control Subcategories
                ("Termite", "Termite control and prevention.", categories["Pest Control Service"]),
                ("Rodent", "Rodent control services.", categories["Pest Control Service"]),
                ("Insect", "Insect pest control.", categories["Pest Control Service"]),

                # Gardening Service Subcategories
                ("Lawn Mowing", "Lawn mowing and trimming.", categories["Gardening and Landscaping Service"]),
                ("Garden Maintenance", "Ongoing garden care.", categories["Gardening and Landscaping Service"]),
                ("Tree Trimming", "Tree and shrub trimming.", categories["Gardening and Landscaping Service"])
            ]

            # Check if each subcategory exists; if not, create it
            for name, description, category in subcategories:
                if not HomeServiceSubCategory.query.filter_by(name=name, category_id=category.category_id).first():
                    subcategory = HomeServiceSubCategory(name=name, description=description, category_id=category.category_id)
                    db.session.add(subcategory)

            db.session.commit()
            print("Home Service Data added successfully!")

# Run the seeding function if this script is executed directly
if __name__ == '__main__':
    seed_data()
