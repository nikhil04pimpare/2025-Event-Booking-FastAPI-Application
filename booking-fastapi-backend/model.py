"""SQLAlchemy ORM models for database tables.

Defines UserModel and EventsModel as SQLAlchemy ORM models that represent
the User and Events tables in the MySQL database.

Classes:
    UserModel: Represents a user in the system with authentication details.
    EventsModel: Represents an event that can be booked by users.
"""

from sqlalchemy import Column, Enum, Integer, String, Date
from database import Base

from schema import UserRole


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
