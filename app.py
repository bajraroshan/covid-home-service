from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from datetime import timedelta
import os

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()  # Initialize without attaching to `app`

def create_app():
    app = Flask(__name__)
    
    # App Configuration
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///covidhomeservice.db'),
        SECRET_KEY=os.getenv('SECRET_KEY', 'your_secret_key'),
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        
        # Mail Configuration
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.getenv('MAIL_USERNAME'),
        MAIL_USE_SSL=False,
        MAIL_DEBUG=True
    )
    
    # Initialize extensions with the app
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)  # Attach Migrate here

    with app.app_context():
        # Import routes and models here to avoid circular imports
        from routes import register_routes
        from models import User, HomeServiceCategory, HomeServiceSubCategory
        
        register_routes(app)
        db.create_all()
        
    return app
