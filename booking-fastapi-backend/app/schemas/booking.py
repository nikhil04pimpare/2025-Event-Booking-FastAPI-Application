"""Pydantic schemas for event management and booking."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Events(BaseModel):
    """Event creation schema.

    Used for creating new events in the system. All fields are required.

    Attributes:
        event_name: Name of the event (string).
        event_venue: Venue/location of the event (string).
        event_date: Date and time of the event (datetime).
        event_availibility: Total number of available seats (integer).
    """

    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int


class EventResponse(BaseModel):
    """Event response schema including the primary key.

    Used when returning event details to clients. Includes all event
    information including the primary key for identification.

    Attributes:
        event_id: Unique event identifier (integer).
        event_name: Name of the event (string).
        event_venue: Venue/location of the event (string).
        event_date: Date and time of the event (datetime).
        event_availibility: Number of currently available seats (integer).
    """

    event_id: int
    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int

    model_config = ConfigDict(from_attributes=True)


class EventBookResponse(BaseModel):
    """Event booking response schema.

    Returned after a successful booking operation. Shows the updated event
    state with remaining available seats after the booking transaction.

    Attributes:
        event_id: Unique event identifier (integer).
        event_name: Name of the event (string).
        event_venue: Venue/location of the event (string).
        event_date: Date and time of the event (datetime).
        event_availibility: Number of remaining available seats after booking (integer).
    """

    event_id: int
    event_name: str
    event_venue: str
    event_date: datetime
    event_availibility: int

    model_config = ConfigDict(from_attributes=True)


class BookingResponse(BaseModel):
    """Response schema for a booking record.

    Represents a single booking transaction. Used by admin endpoints to
    view all bookings in the system with complete details.

    Attributes:
        id: Unique booking identifier (integer).
        user_id: ID of the user who made the booking (integer).
        event_id: ID of the booked event (integer).
        seats_booked: Number of seats reserved in this transaction (integer).
        remaining_tickets: Number of event seats available after this booking (integer).
        booking_time: Timestamp when the booking was created (datetime).
    """

    id: int
    user_id: int
    event_id: int
    seats_booked: int
    remaining_tickets: int
    booking_time: datetime

    model_config = ConfigDict(from_attributes=True)


class EventDetailsForBooking(BaseModel):
    """Schema to show only the required event details in the booking history.

    Lightweight schema used to include event information in booking history
    responses without including unnecessary event fields like availability.

    Attributes:
        event_name: Name of the booked event (string).
        event_date: Date and time of the event (datetime).
    """

    event_name: str
    event_date: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingHistoryResponse(BaseModel):
    """Full booking response schema, including nested event details.

    Complete booking information for user booking history endpoints.
    Includes event details nested within the booking object for convenience.

    Attributes:
        id: Unique booking identifier (integer).
        seats_booked: Number of seats reserved in this transaction (integer).
        remaining_tickets: Number of event seats available after this booking (integer).
        booking_time: Timestamp when the booking was created (datetime).
        event: Nested event details (EventDetailsForBooking) with event name and date.
    """

    id: int
    seats_booked: int
    remaining_tickets: int
    booking_time: datetime

    # This field uses the 'event' relationship we defined in model.py
    event: EventDetailsForBooking

    model_config = ConfigDict(from_attributes=True)
