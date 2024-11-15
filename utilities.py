import bcrypt
import re

def is_valid_phone_number(phone_number):
    pattern = re.compile(r'^\+?[0-9]{10,15}$')
    return re.match(pattern, phone_number) is not None

def generate_password_hash(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)

def verify_password(password, hashed_password):
    # Ensure both password and hashed_password are in bytes
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)
