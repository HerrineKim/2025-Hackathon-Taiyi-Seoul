import secrets
import string
import hashlib
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Password context for hashing API keys
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_api_key_pair():
    """
    Generate a new API key pair (key_id and secret_key)
    """
    # Generate a random key_id (public identifier)
    key_id = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
    
    # Generate a random secret_key
    secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    
    # Hash the secret key for storage
    secret_key_hash = pwd_context.hash(secret_key)
    
    return {
        "key_id": key_id,
        "secret_key": secret_key,
        "secret_key_hash": secret_key_hash
    }

def verify_api_key(plain_secret_key, hashed_secret_key):
    """
    Verify an API key against its hash
    """
    return pwd_context.verify(plain_secret_key, hashed_secret_key)

def calculate_expiry_date(days=365):
    """
    Calculate an expiry date for API keys
    """
    return datetime.utcnow() + timedelta(days=days)
