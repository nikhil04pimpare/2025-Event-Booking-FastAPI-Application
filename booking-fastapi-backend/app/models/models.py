"""SQLAlchemy ORM models for database tables.

Defines UserModel, EventsModel, and BookingModel as SQLAlchemy ORM models
that represent the User, Events, and Bookings tables in the MySQL database.

Classes:
    UserModel: Represents a user in the system with authentication details.
    EventsModel: Represents an event that can be booked by users.
    BookingModel: Represents a booking transaction linking user to event.
"""

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.schemas.user import UserRole


class UserModel(Base):
    """User database model.

    Represents a user account in the system with authentication and role-based
    access control capabilities.

    Attributes:
        id: Primary key, auto-incremented integer.
        name: User's full name (string, up to 255 characters).
        email: User's email address (string, unique constraint).
        password: Hashed password using Argon2 (string, 255 characters).
        role: User's role in the system (enum: admin, user, public).
    """

    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(Enum(UserRole), nullable=False)


class EventsModel(Base):
    """Events database model.

    Represents an event that users can book seats for. Tracks event details
    and available seat inventory.

    Attributes:
        event_id: Primary key, auto-incremented integer.
        event_name: Name of the event (string, up to 255 characters).
        event_venue: Location/venue of the event (string, 255 characters).
        event_date: Date of the event (date type).
        event_availibility: Number of available seats/slots (integer).
    """

    __tablename__ = "Events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String(255))
    event_venue = Column(String(255))
    event_date = Column(Date)
    event_availibility = Column(Integer)


class BookingModel(Base):
    """Booking database model.

    Tracks confirmed ticket reservations, linking a specific user to an event
    and recording the quantity of seats purchased. This model forms the basis
    for the admin tracking system.

    Attributes:
        id: Primary key, auto-incremented integer.
        user_id: Foreign Key linking to the unique ID of the UserModel (the user who made the booking).
        event_id: Foreign Key linking to the event_id of the EventsModel (the event that was booked).
        seats_booked: The number of seats or tickets reserved in this single transaction.
        remaining_tickets: Number of tickets still available after this booking.
        booking_time: Timestamp recording when the booking was successfully created (auto-set).
    """

    __tablename__ = "Bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    event_id = Column(Integer, ForeignKey("Events.event_id"))
    seats_booked = Column(Integer)
    remaining_tickets = Column(Integer)
    booking_time = Column(DateTime, default=func.now())
    event = relationship("EventsModel")
