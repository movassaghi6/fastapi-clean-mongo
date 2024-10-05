from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from core.config import SECRET_KEY, ALGORITHM


# CryptContext instance for password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer instance for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")



def verify_password(plain_password, hashed_password):
    """
    Verifies if the provided plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hashes the provided password using the bcrypt algorithm.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token with an optional expiration time.

    Args:
        data (dict): The data (claims) to encode in the JWT.
        expires_delta (timedelta, optional): The time duration until the token expires. 
                                             Defaults to 15 minutes if not provided.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy() # Copy data to avoid side effects
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire}) # Add expiration claim to token
    # Encode JWT with provided data, secret key, and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

