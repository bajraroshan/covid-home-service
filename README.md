# **COVID Home Service Application**

This repository contains the source code for a Flask-based application that provides essential home services. The features include user authentication, grocery shopping, medication tracking, SOS contact management, and home service requests. The application also integrates email notifications and uses session management for user interactions.

---
## **Student Details**
- Saurab Kharel (a1919868)
- Roshan Bajracharya (a1941176)
- Bidur Dhakal (a1908335)
- Kanak Tanchangya(a1913488)
- Tushar Verma(a1912159)
- Chenfeng Zhu(a1878437)


## **Features**

### **User Management**
- **Signup**: Allows users to register securely with validation for email uniqueness.
- **Login**: Provides secure access for registered users.
- **Logout**: Ends the session securely.
- **Dashboard**: Offers a centralized hub for accessing all services.

### **SOS Contact Management**
- Add, view, and delete emergency contacts.
- Phone number validation for accurate data entry.

### **Medication Management**
- Track and manage medications with schedules.
- Add and delete medications with details such as dosage and frequency.

### **Grocery Shopping**
- Browse grocery items by category.
- Add items to the cart, update quantities, and securely checkout.

### **Home Services**
- Explore home service categories and subcategories.
- Request quotes for specific services, with email notifications sent to the admin.

### **Additional Features**
- Email notifications for quote requests using Flask-Mail.
- Pagination for grocery lists with filter options.
- Secure handling of user sessions and payment details.

---

## **Technologies Used**
- **Backend**: Flask
- **Database**: SQLite (default), configurable to other databases using SQLAlchemy.
- **Frontend**: Jinja2 templates, HTML, CSS.
- **Email Integration**: Flask-Mail for notifications.
- **Environment Variables**: Secure storage for credentials using `python-dotenv`.

---

## **Installation**

### **Requirements**
- Python 3.8 or higher
- pip (Python package manager)

### **Setup**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/bajraroshan/covid-home-service.git
   cd covid-home-service
   ```

2. **Install Dependencies:**
    ```bash 
    pip install -r requirements.txt
    ```

3. **Install Dependencies:**
    ```bash 
    flask db upgrade
    ```

4. **Run the application:**
    ```bash
    python run.py
    ```

5. **Access the application: Open your browser and go to:**
    ```bash
    http://127.0.0.1:5000
    ```

## **Project Structure**

```php
├── app.py              # Application factory and configurations
├── models.py           # Database models
├── routes.py           # Routes and business logic
├── run.py              # Application entry point
├── templates/          # HTML templates
├── static/             # CSS, JS, and images
├── migrations/         # Database migrations
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
```


## Usage

### **Authentication**
- Register using the Signup page.
- Login to access the dashboard.

### **SOS Contacts**
- Manage emergency contacts via the SOS page.

### **Medication Management**
- Add medications with details like doses and schedules.

### **Grocery Shopping**
- Browse items, add to cart, and checkout securely.

### **Home Services**
- Request quotes and manage service categories.

---

## Future Enhancements
- Two-factor authentication (2FA).
- Mobile responsiveness.
- Integration with a payment gateway.
- Notifications for medication schedules.

---

## License
MIT License

Copyright (c) [2024] [Roshan Bajracharya]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
