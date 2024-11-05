from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

class GroceryItem(db.Model):
    __tablename__ = 'grocery_items'
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    grocery_item_id = db.Column(db.Integer, db.ForeignKey('grocery_items.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Helper functions
def generate_password_hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode(), password_hash)

# Landing Page route
@app.route('/')
def landing():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))  # Redirect to dashboard if logged in
    return render_template('landing.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))  # Redirect to dashboard if logged in

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if not email or not password:
            return "Email and password are required", 400

        password_hash = generate_password_hash(password)
        user = User(email=email, username=username, password_hash=password_hash)
        db.session.add(user)
        try:
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            return "Email or username already exists", 409
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))  # Redirect to dashboard if logged in

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Email and password are required", 400

        user = User.query.filter_by(email=email).first()
        if user and verify_password(password, user.password_hash):
            session['user_id'] = user.user_id  # Store user ID in session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password", 401

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    services = [
        {'name': 'SOS', 'url': '/sos'},
        {'name': 'Medicine', 'url': '/medicine'},
        {'name': 'Vital Stat', 'url': '/vital-stat'},
        {'name': 'Food & Groceries', 'url': '/food-groceries'},
        {'name': 'Consultation & Appointment', 'url': '/consult'},
        {'name': 'Home Service', 'url': '/home-service'},
    ]
    return render_template('dashboard.html', services=services)

# Grocery list route
@app.route('/food-groceries')
def food_groceries():
    items = GroceryItem.query.all()
    return render_template('grocery_list.html', items=items)

# Add Grocery Item route
@app.route('/add-grocery', methods=['GET', 'POST'])
def add_grocery():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = float(request.form.get('price'))
        quantity = int(request.form.get('quantity'))

        new_item = GroceryItem(name=name, category=category, price=price, quantity=quantity)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('food_groceries'))

    return render_template('add_grocery.html')


# Add to cart route
@app.route('/add-to-cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    quantity = request.form.get('quantity', type=int)

    # Check if the item is already in the cart
    existing_cart_item = CartItem.query.filter_by(user_id=session['user_id'], grocery_item_id=item_id).first()
    if existing_cart_item:
        # Update the quantity if it already exists
        existing_cart_item.quantity += quantity
    else:
        # Create a new cart item
        cart_item = CartItem(user_id=session['user_id'], grocery_item_id=item_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('food_groceries'))


# View Cart route
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    return render_template('cart.html', cart_items=cart_items)

# Checkout route
@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # You can implement the checkout logic here, such as processing payment or order
    # For now, we will just clear the cart
    CartItem.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    return redirect(url_for('food_groceries'))

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return redirect(url_for('landing'))  # Redirect to the landing page after logout


if __name__ == '__main__':
    app.run(debug=True)
