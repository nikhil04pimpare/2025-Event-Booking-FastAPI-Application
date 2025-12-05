"""FastAPI application for event booking system with user authentication.

This module provides API endpoints for user registration, login, event management,
event booking, and admin booking tracking. It implements JWT-based authentication
and authorization with role-based access control (Admin, User, Public).

Endpoints:
    Authentication: /login
    Users: /users, /users/me
    Events: /events (create, list, book)
    Admin: /admin/bookings (view all bookings)
"""

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db
from app.core.security import (
    CREDENTIALS_EXCEPTION,
    decode_token,
    generate_token,
    hash_password,
    verify_password,
)
from app.models.models import BookingModel, EventsModel, UserModel
from app.schemas.booking import (
    BookingHistoryResponse,
    BookingResponse,
    EventBookResponse,
    EventResponse,
    Events,
)
from app.schemas.user import Token, User, UserLogin, UserResponse, UserRole

Base.metadata.create_all(bind=engine)
oauth2_scheme = HTTPBearer()

app = FastAPI(
    title="Event Booking API",
    description="A FastAPI application for event booking with user authentication",
    version="1.0.0",
)


# ==================== Dependency Functions ====================


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db_session: Session = Depends(get_db),
) -> UserModel:
    """Extract and validate current user from JWT token.

    This function extracts the email from the JWT token and retrieves the
    corresponding user from the database.

    Args:
        token: HTTP Bearer token from request headers.
        db_session: Database session dependency.

    Returns:
        UserModel: Authenticated user object.

    Raises:
        CREDENTIALS_EXCEPTION: If token is invalid or user not found.
    """
    email = decode_token(token.credentials)

    current_user = db_session.query(UserModel).filter(UserModel.email == email).first()

    if not current_user:
        raise CREDENTIALS_EXCEPTION

    return current_user


# ==================== Authentication Endpoints ====================


@app.post("/login", response_model=Token, tags=["Authentication"])
def validate_user(user_info: UserLogin, db_session: Session = Depends(get_db)) -> Token:
    """Authenticate user and generate JWT access token.

    Validates user credentials against the database and generates a JWT token
    for authenticated requests.

    Args:
        user_info: User login credentials (email and password).
        db_session: Database session dependency.

    Returns:
        Token: JWT access token and token type.

    Raises:
        HTTPException: If user not found or password is incorrect.
    """
    current_user = db_session.query(UserModel).filter(UserModel.email == user_info.email).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(user_info.password, current_user.password):
        raise HTTPException(status_code=401, detail="Incorrect Password")

    jwt_token = generate_token(user_info.email)
    return {"access_token": jwt_token, "token_type": "bearer"}


# ==================== User Endpoints ====================


@app.post("/users", response_model=UserResponse, tags=["Users"])
def create_user(user: User, db_session: Session = Depends(get_db)):
    """Create a new user account.

    Registers a new user with the provided details. Password is automatically
    hashed before being stored in the database.

    Args:
        user: User registration data (name, email, password, role).
        db_session: Database session dependency.

    Returns:
        UserResponse: Newly created user object.
    """
    new_user = UserModel(**user.model_dump())

    new_user.password = hash_password(new_user.password)

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user


@app.get("/users/me", tags=["Users"])
def read_current_user(
    current_user: UserModel = Depends(get_current_user),
) -> dict:
    """Retrieve current authenticated user's information.

    Returns detailed information about the authenticated user, including
    name, email, ID, and assigned role.

    Args:
        current_user: Authenticated user from token.

    Returns:
        dict: User's name, ID, email, and role information.
    """
    return {
        "message": f"Welcome back, {current_user.name}! You are logged in with role: {current_user.role}",
        "user_id": current_user.id,
        "email": current_user.email,
    }


# ==================== Event Endpoints ====================


@app.post("/events", response_model=EventResponse, tags=["Events"])
def create_event(
    event: Events,
    db_session: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create a new event.

    Only users with ADMIN role can create new events. The event includes
    details such as name, venue, date, and available slots.

    Args:
        event: Event details (name, venue, date, availability).
        db_session: Database session dependency.
        current_user: Authenticated user from token.

    Returns:
        EventResponse: Newly created event object.

    Raises:
        HTTPException: If user is not authorized to create events.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create event. Must be an Admin",
        )
    new_event = EventsModel(**event.model_dump())
    db_session.add(new_event)
    db_session.commit()
    db_session.refresh(new_event)
    return new_event


@app.get("/events", response_model=list[EventResponse], tags=["Events"])
def get_events(
    db_session: Session = Depends(get_db),
    name: str | None = None,
    venue: str | None = None,
):
    """Retrieve all available events.

    Returns a list of all events in the system, including details such as
    name, venue, date, and available slots.

    Args:
        db_session: Database session dependency.
        name: Name of the event
        venue: Venue of the event

    Returns:
        List[EventResponse]: List of all events.

    Raises:
        HTTPException: If no events are found.
    """
    query = db_session.query(EventsModel)
    if name:
        query = query.filter(EventsModel.event_name.ilike(f"%{name}%"))

    if venue:
        query = query.filter(EventsModel.event_venue.ilike(f"%{venue}%"))

    events = query.all()

    if not events:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No events found.")
    return events


@app.post("/events/{event_id}/book", response_model=EventBookResponse, tags=["Events"])
def book_event(
    event_id: int,
    seats: int,
    db_session: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Book seats for an event.

    Allows authenticated users to book available seats for an event. The
    system checks availability and updates the event's available slots.

    Args:
        event_id: The ID of the event to book.
        seats: Number of seats to book.
        db_session: Database session dependency.
        current_user: Authenticated user from token.

    Returns:
        EventBookResponse: Updated event details after booking.

    Raises:
        HTTPException: If user is not authorized, event not found, or
                       insufficient seats available.
    """
    if current_user.role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to book event. Must be a User",
        )
    event = db_session.query(EventsModel).filter(EventsModel.event_id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No event found. Check event details.",
        )
    if event.event_availibility > 0 and event.event_availibility - seats >= 0:
        event.event_availibility = event.event_availibility - seats

        # Create booking record with remaining tickets after this booking
        booking = BookingModel(
            user_id=current_user.id,
            event_id=event.event_id,
            seats_booked=seats,
            remaining_tickets=event.event_availibility,
        )
        db_session.add(booking)
        db_session.commit()
        db_session.refresh(event)

        return event
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Not able to book event due to lack of availibility",
        )


@app.get("/admin/bookings", response_model=list[BookingResponse], tags=["Admin"])
def get_admin_bookings(
    db_session: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Retrieve all booking records (Admin only).

    Allows administrators to view all booking transactions in the system.
    Returns detailed information about each booking including user, event,
    seats booked, and booking timestamp.

    Args:
        db_session: Database session dependency.
        current_user: Authenticated user from token.

    Returns:
        List[BookingResponse]: List of all booking records.

    Raises:
        HTTPException: If user is not authorized (must be Admin) or
                       no bookings are found in the system.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to check bookings. Must be an Admin",
        )
    bookings = db_session.query(BookingModel).all()
    if not bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Bookings found.")
    return bookings


@app.get("/users/me/bookings", response_model=list[BookingHistoryResponse], tags=["User"])
def get_user_bookings(
    db_session: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Retrieve current user's booking history.

    Returns all bookings made by the authenticated user, including detailed
    information about each booking and the associated event details.

    Args:
        db_session: Database session dependency.
        current_user: Authenticated user from token.

    Returns:
        List[BookingHistoryResponse]: List of user's booking records with
                                      nested event information.

    Raises:
        HTTPException: If no bookings are found for the current user.
    """
    bookings = (
        db_session.query(BookingModel)
        .join(BookingModel.event)
        .filter(current_user.id == BookingModel.user_id)
        .all()
    )

    if not bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Bookings found.")

    return bookings
