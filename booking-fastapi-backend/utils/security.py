"""Security utilities for authentication and authorization.

Provides password hashing, JWT token generation/validation, and related
security functions for the booking application.

Configuration:
    SECRET_KEY: Secret key for signing JWT tokens. Should be moved to
                environment variables in production.
    ALGORITHM: Algorithm used for JWT encoding/decoding (HS256).
    ACCESS_TOKEN_EXPIRE_MINUTE: Token expiration time in minutes (default: 30).
    pwd_context: Password hashing context using Argon2 algorithm.
    CREDENTIALS_EXCEPTION: Standard HTTP exception for authentication failures.

Functions:
    hash_password: Hash a plain text password using Argon2.
    verify_password: Verify a plain text password against a hashed password.
    generate_token: Generate a JWT access token for user authentication.
    decode_token: Decode and validate a JWT access token.
"""

from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException, status
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


def hash_password(password: str) -> str:
    """Hash a plain text password using Argon2.

    Converts a plain text password into a secure hashed format using the
    Argon2 algorithm. This hashed password is stored in the database.

    Args:
        password: Plain text password to hash (string).

    Returns:
        str: Hashed password as a string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password.

    Compares a plain text password provided by the user against a previously
    hashed password stored in the database using Argon2 verification.

    Args:
        plain_password: Plain text password from user input (string).
        hashed_password: Hashed password from database (string).

    Returns:
        bool: True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(email: str) -> str:
    """Generate a JWT access token for user authentication.

    Creates a JWT token containing the user's email and expiration time.
    The token can be used for subsequent authenticated requests.

    Args:
        email: User's email to encode in token (string).

    Returns:
        str: Encoded JWT token as a string.

    Token Payload:
        sub: User's email (subject claim).
        exp: Token expiration time (expiration claim).
        iat: Token issued at time (issued at claim).
    """
    payload = {
        "sub": email,
        "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE),
        "iat": datetime.now(UTC),
    }

    # Encode JWT with secret key using specified algorithm
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_token(token: str) -> str:
    """Decode and validate a JWT access token.

    Extracts the email from a JWT token and validates its signature and
    expiration. Raises an exception if the token is invalid, expired, or
    corrupted.

    Args:
        token: JWT token to decode (string).

    Returns:
        str: Email extracted from token payload.

    Raises:
        CREDENTIALS_EXCEPTION: If token is expired, has invalid signature,
                               or is corrupted/malformed.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload.get("sub")
    except jwt.exceptions.ExpiredSignatureError:
        raise CREDENTIALS_EXCEPTION from None

    except jwt.exceptions.InvalidSignatureError:
        raise CREDENTIALS_EXCEPTION from None

    except jwt.exceptions.PyJWTError:
        raise CREDENTIALS_EXCEPTION from None
