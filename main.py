"""FastAPI application for event booking system with user authentication.

This module provides API endpoints for user registration, login, and retrieving
current user information. It implements JWT-based authentication and authorization.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from model import UserModel, EventsModel
from schema import Token, User, Events, UserLogin
from utils.security import CREDENTIALS_EXCEPTION, decode_token, generate_token, hash_password, verify_password

Base.metadata.create_all(bind=engine)
oauth2_scheme = HTTPBearer()

app = FastAPI()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db_session: Session = Depends(get_db)):
    """Extract and validate current user from JWT token.
    
    Args:
        token: HTTP Bearer token from request headers
        db_session: Database session dependency
        
    Returns:
        UserModel: Authenticated user object
        
    Raises:
        CREDENTIALS_EXCEPTION: If token is invalid or user not found
    """
    email = decode_token(token.credentials)

    current_user = db_session.query(UserModel).filter(UserModel.email == email).first()

    if not current_user:
        raise CREDENTIALS_EXCEPTION

    return current_user


@app.get("/users/me")
def read_current_user(current_user: UserModel = Depends(get_current_user)):
    """Retrieve current authenticated user's information.
    
    Args:
        current_user: Authenticated user from token
        
    Returns:
        dict: User's name, ID, email, and role information
    """
    return {
        "message": f"Welcome back, {current_user.name}! You are logged in with role: {current_user.role}",
        "user_id": current_user.id,
        "email": current_user.email
    }


@app.post("/login", response_model=Token)
def validate_user(user_info: UserLogin, db_session: Session = Depends(get_db)):
    """Authenticate user and generate JWT access token.
    
    Args:
        user_info: User login credentials (email and password)
        db_session: Database session dependency
        
    Returns:
        Token: JWT access token and token type
        
    Raises:
        HTTPException: If user not found or password incorrect
    """
    current_user = db_session.query(UserModel).filter(UserModel.email == user_info.email).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(user_info.password, current_user.password):
        raise HTTPException(status_code=401, detail="Incorrect Password")
    
    jwt_token = generate_token(user_info.email)
    return {"access_token":jwt_token, "token_type":"bearer"}


@app.post("/users")
def create_user(user: User, db_session: Session = Depends(get_db)):
    """Create a new user account.
    
    Args:
        user: User registration data (name, email, password, role)
        db_session: Database session dependency
        
    Returns:
        UserModel: Newly created user object
    """
    new_user = UserModel(**user.model_dump())

    new_user.password = hash_password(new_user.password)

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user