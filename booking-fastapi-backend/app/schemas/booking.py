"""Pydantic schemas for event management and booking."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Events(BaseModel):
    """Event creation schema."""

    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int


class EventResponse(BaseModel):
    """Event response schema including the primary key."""

    event_id: int
    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int

    model_config = ConfigDict(from_attributes=True)


class EventBookResponse(BaseModel):
    """Event booking response schema."""

    event_id: int
    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int

    model_config = ConfigDict(from_attributes=True)


class BookingResponse(BaseModel):
    """Response schema for a booking record."""

    id: int
    user_id: int
    event_id: int
    seats_booked: int
    remaining_tickets: int
    booking_time: datetime

    model_config = ConfigDict(from_attributes=True)
