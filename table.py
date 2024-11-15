from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

# Initialize Flask app
app = Flask(__name__)

# Configuration for the database located in the instance folder
import os

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('instance/covidhomeservice.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Function to print the database structure
def print_db_structure():
    with app.app_context():
        inspector = inspect(db.engine)
        # Loop through each table in the database
        for table_name in inspector.get_table_names():
            print(f"Table: {table_name}")
            # Retrieve and print column details
            columns = inspector.get_columns(table_name)
            for column in columns:
                print(f"    Column: {column['name']}, Type: {column['type']}")

# Run the function to print the database structure
if __name__ == '__main__':
    print_db_structure()
