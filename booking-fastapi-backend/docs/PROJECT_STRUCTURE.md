# Project Structure

```
booking-fastapi-backend/
├── app/                              # Main application package
│   ├── __init__.py
│   ├── main.py                      # FastAPI app with all endpoints
│   ├── api/                         # API routes (future expansion)
│   │   └── __init__.py
│   ├── core/                        # Core utilities
│   │   ├── __init__.py
│   │   ├── database.py             # SQLAlchemy setup, session management
│   │   └── security.py             # JWT, password hashing utilities
│   ├── models/                      # Database ORM models
│   │   ├── __init__.py
│   │   └── models.py               # UserModel, EventsModel, BookingModel
│   └── schemas/                     # Pydantic validation schemas
│       ├── __init__.py
│       ├── user.py                 # User, UserLogin, UserResponse, Token
│       └── booking.py              # Events, Bookings, EventResponse schemas
│
├── docs/                            # Documentation
│   ├── PROJECT_STRUCTURE.md        # This file
│   ├── API_ENDPOINTS.md            # Complete API documentation
│   └── SETUP.md                    # Development setup guide
│
├── main.py                         # Entry point (imports app from app.main)
├── .vscode/
│   └── launch.json                # VS Code debugging configuration
├── .editorconfig                  # Cross-editor configuration
├── .gitignore                     # Git ignore rules
├── .pre-commit-config.yaml        # Pre-commit hooks
├── pyproject.toml                 # Project metadata & dependencies
├── uv.lock                        # Dependency lock file
├── Makefile                       # Linux/macOS development commands
├── dev.bat                        # Windows development commands
├── README.md                      # Main project documentation
├── docker-compose.yml             # Docker compose configuration
└── .gitattributes                 # Git attributes
```

## Architecture Overview

### Layer Structure

```
API Layer (app/main.py)
    ↓
Core Services (app/core/)
    ├── Security (JWT, password hashing)
    └── Database (SQLAlchemy sessions)
    ↓
Models (app/models/models.py)
    ├── UserModel
    ├── EventsModel
    └── BookingModel
    ↓
Schemas (app/schemas/)
    ├── User schemas
    └── Booking schemas
    ↓
Database (MySQL)
```

## Key Components

### app/core/
- **database.py**: SQLAlchemy engine, session factory, dependency injection
- **security.py**: JWT token generation/validation, password hashing with Argon2

### app/models/
- **models.py**: SQLAlchemy ORM models for User, Events, and Bookings tables

### app/schemas/
- **user.py**: Pydantic models for user-related endpoints (registration, login, responses)
- **booking.py**: Pydantic models for events and booking-related endpoints

### app/api/
- Reserved for organizing endpoint groups by feature (authentication, events, bookings)
- Can be extended with router files (routers.py)

## Development Workflow

1. **Local Development**: Use `.\dev.bat dev` (Windows) or `make dev` (Linux/macOS)
2. **Debugging**: Use VS Code F5 to attach debugger
3. **Code Quality**: Pre-commit hooks run automatically before commits
4. **Testing**: Run `.\dev.bat test` or `make test`

## Adding New Features

### Adding a new endpoint:
1. Create/modify route in `app/main.py` or create router in `app/api/`
2. Create corresponding schema in `app/schemas/` if needed
3. Add model to `app/models/models.py` if new table required
4. Ensure imports are updated correctly

### Example:
```python
# app/main.py
from app.schemas.new_feature import NewFeatureSchema
from app.models.models import NewFeatureModel

@app.post("/new-endpoint", response_model=NewFeatureSchema)
def create_feature(data: NewFeatureSchema, db_session: Session = Depends(get_db)):
    # Implementation
    pass
```

## Scalability Notes

- **Routers**: Move related endpoints to separate files in `app/api/` as project grows
- **Database**: Switch to async driver (asyncpg) if high concurrency needed
- **Caching**: Add Redis for session/token caching
- **Microservices**: Extract event/booking logic into separate services if needed
