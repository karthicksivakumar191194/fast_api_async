import random
import string
from passlib.context import CryptContext

# Create a password context using bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes the given password using a secure hashing algorithm.
    """
    return pwd_context.hash(password)


def generate_random_string(length: int = 4) -> str:
    """
    Generates a random string of a specified length.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))