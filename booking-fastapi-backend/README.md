# Event Booking FastAPI

A simple, production-ready REST API for event booking with JWT authentication.

## Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Setup database (MySQL required)
# Update DB_URL in app/core/database.py if needed

# 3. Run application
uvicorn app.main:app --reload

# Or on Windows
.\dev.bat dev
```

API available at: http://localhost:8000/docs

## Project Structure

```
app/
├── core/          # Database & security utilities
├── models/        # SQLAlchemy ORM models
├── schemas/       # Pydantic validation schemas
├── api/           # Route modules (ready for expansion)
└── main.py        # FastAPI application

docs/
├── API.md         # API endpoint reference
```

## Features

- ✅ User registration & JWT authentication
- ✅ Event creation & listing with search filters
- ✅ Event booking with automatic inventory tracking
- ✅ User booking history with event details
- ✅ Admin booking management and tracking
- ✅ Role-based access control (Admin, User)
- ✅ Argon2 password hashing
- ✅ Code quality tools (Black, isort, Ruff, Mypy)
- ✅ Pre-commit hooks for automation

## API Endpoints

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/login` | ❌ | User login |
| POST | `/users` | ❌ | Register user |
| GET | `/users/me` | ✅ | Get profile |
| POST | `/events` | ✅ | Create event (Admin) |
| GET | `/events` | ❌ | List events |
| POST | `/events/{id}/book` | ✅ | Book event |
| GET | `/admin/bookings` | ✅ | View all bookings (Admin) |
| GET | `/users/me/bookings` | ✅ | View my bookings (User) |

See `docs/API.md` for detailed examples.

## Installation

### Prerequisites
- Python 3.11+
- MySQL 5.7+
- UV package manager

### With Docker (MySQL)

```bash
docker-compose up -d
uv sync
uvicorn app.main:app --reload
```

### Without Docker

Create MySQL database:
```sql
CREATE DATABASE task_db;
CREATE USER 'api_user'@'localhost' IDENTIFIED BY 'api_password';
GRANT ALL PRIVILEGES ON task_db.* TO 'api_user'@'localhost';
FLUSH PRIVILEGES;
```

Then:
```bash
uv sync
uvicorn app.main:app --reload
```

## Database Models

### User
- `id` (int) - Primary key
- `name` (str) - User name
- `email` (str) - Unique email
- `password` (str) - Argon2 hashed
- `role` (str) - Admin | User | Public

### Events
- `event_id` (int) - Primary key
- `event_name` (str) - Event name
- `event_venue` (str) - Event location
- `event_date` (datetime) - Event date
- `event_availibility` (int) - Total tickets

### Bookings
- `id` (int) - Primary key
- `user_id` (int) - Foreign key → User
- `event_id` (int) - Foreign key → Events
- `seats_booked` (int) - Number of seats
- `remaining_tickets` (int) - Available after booking
- `booking_time` (datetime) - Auto-timestamp

## Development

### Code Quality

```bash
# Windows
.\dev.bat quality    # Run all checks

# Linux/macOS
make quality         # Run all checks
```

Checks include: Black (formatting), isort (imports), Ruff (linting), Mypy (type checking).

### Install Pre-commit Hooks

```bash
# Windows
.\dev.bat precommitinstall

# Linux/macOS
make pre-commit-install
```

### Run Tests

```bash
pytest -v
```

## Configuration

Edit `app/core/database.py` to change database URL:

```python
DB_URL = "mysql+pymysql://user:password@host:port/database"
```

For production, use environment variables:

```python
import os
DB_URL = os.getenv("DATABASE_URL", "mysql+pymysql://api_user:api_password@localhost:3306/task_db")
```

## Security

- Passwords hashed with Argon2 (GPU-resistant)
- JWT tokens with 30-minute expiration
- Role-based access control implemented
- Bandit security scanning enabled

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **Auth**: JWT + Argon2
- **Validation**: Pydantic v2
- **Package Manager**: UV

## License

MIT License

## Support

Check `docs/API.md` for endpoint examples and error codes.
