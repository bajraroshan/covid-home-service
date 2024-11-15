from flask import request, render_template, redirect, url_for, session
from flask_mail import Message
from sqlalchemy.exc import IntegrityError
from sqlalchemy import distinct
from math import ceil
from models import User, HomeServiceCategory, HomeServiceSubCategory, SOSContact, Medication, GroceryItem, CartItem
from utilities import is_valid_phone_number, generate_password_hash, verify_password
from app import mail, db

def register_routes(app):
    # LANDING PAGE
    @app.route('/')
    def landing():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return render_template('landing.html')
    
    # SIGNUP PAGE
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            address = request.form.get('address')
            mobile_number = request.form.get('mobile_number')
            phone_number = request.form.get('phone_number')
            country = request.form.get('country')
            language = request.form.get('language')
            vaccinated = request.form.get('vaccinated')
            occupation = request.form.get('occupation')
            credit_card_number = request.form.get('credit_card_number')
            expiry_date = request.form.get('expiry_date')
            cvv = request.form.get('cvv')

            if password != confirm_password:
                return render_template('signup.html', error="Passwords do not match")
            if not all([email, password, mobile_number]):
                return render_template('signup.html', error="Required fields are missing")
            if not is_valid_phone_number(mobile_number):
                return render_template('signup.html', error="Invalid mobile number format")

            password_hash = generate_password_hash(password)
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=password_hash,
                address=address,
                mobile_number=mobile_number,
                phone_number=phone_number,
                country=country,
                language=language,
                vaccinated=vaccinated,
                occupation=occupation,
                credit_card_number=credit_card_number,
                expiry_date=expiry_date,
                cvv=cvv
            )
            db.session.add(user)
            try:
                db.session.commit()
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                return render_template('signup.html', error="Email already exists")

        return render_template('signup.html')
    
    # LOGIN PAGE
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and verify_password(password, user.password_hash):
                session['user_id'] = user.user_id
                session.permanent = True
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Invalid email or password")

        return render_template('login.html')

    # Dashboard PAGE
    @app.route('/dashboard')
    def dashboard():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        user = db.session.get(User, user_id)
        if not user:
            session.pop('user_id', None)
            return redirect(url_for('login'))

        services = [
            {'name': 'SOS', 'url': '/sos', 'icon': 'telephone'},
            {'name': 'Medicine', 'url': '/medicine', 'icon': 'capsule-pill'},
            {'name': 'Food & Groceries', 'url': '/grocery-list', 'icon': 'cart'},
            {'name': 'Consultation & Appointment', 'url': 'https://universityhealthpractice.com.au/', 'icon': 'calendar3'},
            {'name': 'Home Service', 'url': '/home-services', 'icon': 'house-door-fill'},
        ]
        return render_template('dashboard.html', services=services, user=user)
    

    # SOS PAGE
    @app.route('/sos', methods=['GET', 'POST'])
    def sos():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        user = User.query.get(user_id)
        contacts = SOSContact.query.filter_by(user_id=user_id).all()

        if request.method == 'POST':
            # Handle add contact logic
            if 'delete_contact' in request.form:
                contact_id = request.form.get('delete_contact')
                contact = SOSContact.query.get(contact_id)
                if contact and contact.user_id == user_id:
                    db.session.delete(contact)
                    db.session.commit()
                return redirect(url_for('sos'))
            else:
                # Handle add new contact logic
                name = request.form.get('name')
                phone = request.form.get('phone')
                relationship = request.form.get('relationship')
                if not phone or not phone.isdigit():
                    return render_template('sos_contacts.html', user=user, contacts=contacts, error="Phone number must contain only digits")
                new_contact = SOSContact(user_id=user_id, name=name, phone=phone, relationship=relationship)
                db.session.add(new_contact)
                db.session.commit()
                return redirect(url_for('sos'))

        return render_template('sos.html', user=user, contacts=contacts)
    
    # MEDICINE PAGE
    @app.route('/medicine', methods=['GET'])
    def view_medications():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        medications = Medication.query.filter_by(user_id=session['user_id']).all()

        # Extract medication times as a list of strings
        medication_times = [med.times for med in medications if med.times]

        return render_template('medications.html', medications=medications, medication_times=medication_times)


    @app.route('/add-medication', methods=['GET', 'POST'])
    def add_medication():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            try:
                name = request.form.get('name')
                doses_per_day = int(request.form.get('doses_per_day'))
                frequency = request.form.get('frequency')
                duration = int(request.form.get('duration'))
                times = request.form.get('times')

                if not all([name, doses_per_day, frequency, duration, times]):
                    return render_template('add_medication.html', 
                                        error="All fields are required")

                new_medication = Medication(
                    user_id=session['user_id'],
                    name=name,
                    doses_per_day=doses_per_day,
                    frequency=frequency,
                    duration=duration,
                    times=times
                )
                db.session.add(new_medication)
                db.session.commit()
                return redirect(url_for('view_medications'))
            except ValueError:
                return render_template('add_medication.html', 
                                    error="Invalid input values")

        return render_template('add_medication.html')

    @app.route('/delete-medication/<int:medication_id>', methods=['POST'])
    def delete_medication(medication_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))

        medication = Medication.query.get_or_404(medication_id)
        if medication.user_id == session['user_id']:
            db.session.delete(medication)
            db.session.commit()
        return redirect(url_for('view_medications'))
    
    # GROCERIES PAGE
    @app.route('/grocery-list', methods=['GET'])
    def grocery_list():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        items_per_page = 12
        page = request.args.get('page', 1, type=int)
        selected_category = request.args.get('category', None)

        # Fetch distinct categories for the dropdown
        categories_query = db.session.query(GroceryItem.category.distinct()).all()
        categories = [c[0] for c in categories_query]  # Extract category names from tuples

        # Filter items by selected category if provided
        if selected_category:
            items_query = GroceryItem.query.filter_by(category=selected_category).order_by(GroceryItem.name.asc())
        else:
            items_query = GroceryItem.query.order_by(GroceryItem.name.asc())

        total_items = items_query.count()

        # Pagination logic
        items = items_query.offset((page - 1) * items_per_page).limit(items_per_page).all()
        total_pages = ceil(total_items / items_per_page)
        pagination = {
            "current_page": page,
            "prev_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if page < total_pages else None,
            "pages": list(range(1, total_pages + 1)),
        }

        return render_template('grocery_list.html', items=items, pagination=pagination, categories=categories, selected_category=selected_category)





    # Add to cart route
    @app.route('/add-to-cart/<int:item_id>', methods=['POST'])
    def add_to_cart(item_id):
        
        # Check if user is logged in
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in

        # Retrieve the quantity from the form
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

        # Get the current page from the query parameters
        current_page = request.args.get('page', 1, type=int)

        # Redirect back to the same page with pagination
        return redirect(url_for('grocery_list', page=current_page))




    # View Cart route
    @app.route('/cart')
    def cart():
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in

        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        return render_template('cart.html', cart_items=cart_items)
    
    @app.route('/remove-from-cart/<int:cart_item_id>', methods=['POST'])
    def remove_from_cart(cart_item_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in

        cart_item = CartItem.query.get(cart_item_id)
        if cart_item and cart_item.user_id == session['user_id']:
            db.session.delete(cart_item)
            db.session.commit()
        return redirect(url_for('cart'))
    
    # Update quantity in cart route
    @app.route('/update-cart/<int:cart_item_id>', methods=['POST'])
    def update_cart(cart_item_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in

        # Fetch the cart item
        cart_item = CartItem.query.get_or_404(cart_item_id)
        
        if cart_item.user_id != session['user_id']:
            return redirect(url_for('cart'))  # Prevent unauthorized access

        # Get the updated quantity from the form
        updated_quantity = request.form.get('quantity', type=int)

        if updated_quantity <= 0:
            # Remove the item if quantity is set to 0 or less
            db.session.delete(cart_item)
        else:
            # Update the quantity
            cart_item.quantity = updated_quantity

        db.session.commit()
        return redirect(url_for('cart'))


   # Checkout Page
    @app.route('/checkout', methods=['GET', 'POST'])
    def checkout():
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in

        return redirect(url_for('payment_confirmation'))  # Redirect to the payment confirmation page




    # Checkout Success Page
    @app.route('/checkout-success')
    def checkout_success():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return render_template('checkout_success.html')
    
    # Payment Confirmation Page
    @app.route('/payment-confirmation', methods=['GET', 'POST'])
    def payment_confirmation():
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect to login if not logged in

        # Fetch user and cart details
        user = User.query.get(session['user_id'])
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        total_cost = sum(item.quantity * item.grocery_item.price for item in cart_items)

        if request.method == 'POST':
            # Retrieve and validate payment details from form submission
            card_number = request.form.get('card_number')
            expiry_date = request.form.get('expiry_date')
            cvv = request.form.get('cvv')

            # Process the payment logic here (e.g., payment gateway integration)
            # For now, clear the cart after payment
            CartItem.query.filter_by(user_id=session['user_id']).delete()
            db.session.commit()

            return render_template('checkout_success.html', total_cost=total_cost)

        return render_template('payment_confirmation.html', total_cost=total_cost, user=user)



    # HOME SERVICE PAGE
    @app.route('/home-services')
    def home_service():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        categories = HomeServiceCategory.query.all()
        return render_template('home_service.html', categories=categories)

    @app.route('/subcategories/<int:category_id>')
    def subcategory_list(category_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        category = HomeServiceCategory.query.get_or_404(category_id)
        return render_template('subcategory_list.html', category=category)

    @app.route('/quote/<int:subcategory_id>', methods=['GET', 'POST'])
    def quote_request(subcategory_id):
        # Get the current user
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))
        
        user = User.query.get(user_id)
        subcategory = HomeServiceSubCategory.query.get_or_404(subcategory_id)
        
        if request.method == 'POST':
            user_details = request.form.get('details')
            preferred_date = request.form.get('date')
            preferred_time = request.form.get('time')
            
            msg = Message(
                subject=f"New Quote Request for {subcategory.name}",
                sender=(f"{user.first_name} {user.last_name}", app.config['MAIL_USERNAME']),  # Add name here
                recipients=[app.config['MAIL_USERNAME']],
                body=f"""
                From: {user.first_name} {user.last_name}
                Email: {user.email}
                Phone: {user.mobile_number}
                
                Service: {subcategory.name}
                Details: {user_details}
                Preferred Date: {preferred_date}
                Preferred Time: {preferred_time}
                """
            )
            
            try:
                mail.send(msg)
                return redirect(url_for('thank_you'))
            except Exception as e:
                return f"An error occurred: {e}"
        
        return render_template('quote_form.html', subcategory=subcategory, user=user)

    @app.route('/thank_you', methods=['GET'])
    def thank_you():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return render_template('thank_you.html')

    @app.route('/logout', methods=['POST'])
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('landing'))