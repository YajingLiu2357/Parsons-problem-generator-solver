import hashlib

def hash_password(password, password_encoding_salt):
    """Hash a password for storing."""
    hashed = hashlib.sha256((password + password_encoding_salt).encode('utf-8')).hexdigest()
    return hashed