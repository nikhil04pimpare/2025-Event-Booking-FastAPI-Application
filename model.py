"""SQLAlchemy ORM models for database tables.

Defines UserModel and EventsModel as representations of User and Events
tables in the database.
"""

from sqlalchemy import Column, Integer, String, Date
from database import Base


class UserModel(Base):
    """User database model.
    
    Attributes:
        id: Primary key, auto-incremented integer
        name: User's full name
        email: User's email, unique constraint
        password: Hashed password
        role: User's role (e.g., admin, user)
    """
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(String(255))


class EventsModel(Base):
    """Events database model.
    
    Attributes:
        event_id: Primary key, auto-incremented integer
        event_name: Name of the event
        event_venue: Location where event will be held
        event_date: Date of the event
        event_availibility: Number of available seats/slots
    """
    __tablename__ = "Events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String(255))
    event_venue = Column(String(255))
    event_date = Column(Date)
    event_availibility = Column(Integer)
