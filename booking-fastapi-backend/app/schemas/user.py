"""Pydantic schemas for user authentication and responses."""

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
    """User registration schema."""

    name: str
    email: str
    password: str = Field(max_length=72)
    role: UserRole


class UserLogin(BaseModel):
    """User login credentials schema."""

    email: str
    password: str


class UserResponse(BaseModel):
    """User response schema including the primary key."""

    id: int
    name: str
    email: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT token response schema."""

    access_token: str
    token_type: str
