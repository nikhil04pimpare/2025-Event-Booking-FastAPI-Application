"""Pydantic schemas for request/response validation.

Defines data models for API endpoints with automatic validation and
documentation generation.
"""

from pydantic import BaseModel, Field
from datetime import datetime


class User(BaseModel):
    """User registration schema.
    
    Attributes:
        name: User's full name
        email: User's email address
        password: Password (max 72 characters for security)
        role: User's role in the system
    """
    name: str
    email: str
    password: str = Field(max_length=72)
    role: str

# event validation
class Events(BaseModel):
    """Event creation schema.
    
    Attributes:
        event_name: Name of the event
        event_venue: Venue/location of the event
        event_date: Date and time of the event
        event_availibility: Number of available slots
    """
    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int

class UserLogin(BaseModel):
    """User login credentials schema.
    
    Attributes:
        email: User's registered email
        password: User's password
    """
    email: str
    password: str

class Token(BaseModel):
    """JWT token response schema.
    
    Attributes:
        access_token: JWT token for authenticated requests
        token_type: Type of token (typically 'bearer')
    """
    access_token: str
    token_type: str