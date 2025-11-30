"""Security utilities for authentication and authorization.

Provides password hashing, JWT token generation/validation, and related
security functions for the booking application.
"""

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Configuration
SECRET_KEY = "your-super-secret-key"  # TODO: Move to environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_password(password: str):
    """Hash a plain text password using Argon2.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Verify a plain text password against a hashed password.
    
    Args:
        plain_password: Plain text password from user
        hashed_password: Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(email: str):
    """Generate a JWT access token for user authentication.
    
    Args:
        email: User's email to encode in token
        
    Returns:
        str: Encoded JWT token
    """
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE),
        "iat": datetime.now(timezone.utc)
    }

    # Encode JWT with secret key
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_token(token: str):
    """Decode and validate a JWT access token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        str: Email extracted from token payload
        
    Raises:
        CREDENTIALS_EXCEPTION: If token is expired, invalid, or corrupted
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload.get("sub")
    except jwt.exceptions.ExpiredSignatureError:
        raise CREDENTIALS_EXCEPTION

    except jwt.exceptions.InvalidSignatureError:
        raise CREDENTIALS_EXCEPTION
        
    except jwt.exceptions.PyJWTError:
        raise CREDENTIALS_EXCEPTION