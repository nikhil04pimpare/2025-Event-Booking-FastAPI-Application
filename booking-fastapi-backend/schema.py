"""Pydantic schemas for request/response validation.

Defines data models for API endpoints with automatic validation and
documentation generation. Includes enums for user roles and schemas for
authentication, user management, and event booking.

Enums:
    UserRole: Enum for user roles (admin, user, public).

Classes:
    User: User registration schema.
    UserLogin: User login credentials schema.
    Token: JWT token response schema.
    Events: Event creation schema.
    EventResponse: Event response schema with ORM mapping.
    EventBookResponse: Event booking response schema with ORM mapping.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class UserRole(Enum):
    """Enumeration of user roles in the system.

    Attributes:
        ADMIN: Administrator role with full privileges (create events).
        USER: Regular user role (can book events).
        PUBLIC: Public role with limited access.
    """

    ADMIN = "admin"
    USER = "user"
    PUBLIC = "public"


class User(BaseModel):
    """User registration schema.

    Used for validating user registration requests. Defines required fields
    and validation constraints.

    Attributes:
        name: User's full name (string).
        email: User's email address (string).
        password: Password for the user account (max 72 characters for security).
        role: User's role in the system (UserRole enum).
    """

    name: str
    email: str
    password: str = Field(max_length=72)
    role: UserRole


class UserLogin(BaseModel):
    """User login credentials schema.

    Used for validating login requests with email and password.

    Attributes:
        email: User's registered email address (string).
        password: User's password (string).
    """

    email: str
    password: str


class UserResponse(BaseModel):
    """User response schema including the primary key.

    Used for returning user details in API responses. Includes user
    information with ORM model mapping for automatic attribute conversion.

    Attributes:
        id: Primary key of the user (integer).
        name: User's full name (string).
        email: User's email address (string).
        role: User's role in the system (UserRole enum).
    """

    id: int
    name: str
    email: str
    role: UserRole

    # Configuration for mapping ORM model attributes to schema
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT token response schema.

    Returned when a user successfully authenticates. Contains the JWT token
    and its type.

    Attributes:
        access_token: JWT token for authenticated requests (string).
        token_type: Type of token, typically 'bearer' (string).
    """

    access_token: str
    token_type: str


class Events(BaseModel):
    """Event creation schema.

    Used for validating event creation requests. Defines event details
    including venue, date, and availability.

    Attributes:
        event_name: Name of the event (string).
        event_venue: Venue/location of the event (string).
        event_date: Date and time of the event (datetime).
        event_availibility: Number of available seats/slots (integer).
    """

    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int


class EventResponse(BaseModel):
    """Event response schema including the primary key.

    Used for returning event details in API responses. Includes all event
    information with ORM model mapping for automatic attribute conversion.

    Attributes:
        event_id: Primary key of the event (integer).
        event_name: Name of the event (string).
        event_venue: Venue/location of the event (string).
        event_date: Date and time of the event (datetime).
        event_availibility: Number of available seats/slots (integer).
    """

    event_id: int
    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int

    # Configuration for mapping ORM model attributes to schema
    model_config = ConfigDict(from_attributes=True)


class EventBookResponse(BaseModel):
    """Event booking response schema including the primary key.

    Returned after a successful event booking. Includes updated event details
    with remaining availability after booking.

    Attributes:
        event_id: Primary key of the event (integer).
        event_name: Name of the event (string).
        event_venue: Venue/location of the event (string).
        event_date: Date and time of the event (datetime).
        event_availibility: Remaining available seats/slots after booking (integer).
    """

    event_id: int
    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int

    # Configuration for mapping ORM model attributes to schema
    model_config = ConfigDict(from_attributes=True)


class BookingResponse(BaseModel):
    """Response schema for a booking record.

    Includes booking details with user, event, seats booked, remaining tickets
    after booking, and booking timestamp.

    Attributes:
        id: Primary key of the booking (integer).
        user_id: ID of the user who made the booking (integer).
        event_id: ID of the event that was booked (integer).
        seats_booked: Number of seats booked in this transaction (integer).
        remaining_tickets: Number of tickets still available after this booking (integer).
        booking_time: Timestamp of when the booking was made (datetime).
    """

    id: int
    user_id: int
    event_id: int
    seats_booked: int
    remaining_tickets: int
    booking_time: datetime

    model_config = ConfigDict(from_attributes=True)
