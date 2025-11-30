# Event Booking FastAPI Application

A FastAPI-based REST API for managing event bookings with user authentication using JWT tokens.

## Overview

This application provides a comprehensive event booking system with:
- User registration, authentication, and role-based access control
- JWT-based authorization with configurable token expiration
- Event management with availability tracking
- Secure event booking with inventory management
- SQLAlchemy ORM with MySQL database integration
- Secure password hashing using Argon2
- Comprehensive API documentation via Swagger UI

## Project Structure

```
booking-fastapi/
├── __init__.py                # Package initialization
├── main.py                    # FastAPI application and route handlers
├── database.py               # Database configuration and session management
├── model.py                  # SQLAlchemy ORM models (User, Events)
├── schema.py                 # Pydantic validation schemas
└── utils/
    ├── __init__.py
    └── security.py           # Authentication and security utilities
```

## Features

### Authentication & Security
- **Password Hashing**: Argon2-based secure password hashing
- **JWT Tokens**: Bearer token authentication with configurable expiration
- **Token Expiration**: Configurable token expiry (default: 30 minutes)
- **Secure Credentials**: HTTPBearer scheme for token transmission
- **Role-Based Access Control**: Admin, User, and Public roles

### Event Management
- **Create Events**: Admin-only endpoint for event creation
- **Event Listing**: Public access to available events
- **Event Booking**: User-only endpoint to book event seats
- **Inventory Tracking**: Automatic availability management
- **Conflict Prevention**: Prevents overbooking with availability checks

### Core Models

#### UserModel
- Unique email-based identification
- Hashed password storage using Argon2
- Role-based access control (Admin, User, Public)
- Auto-incremented primary key

#### EventsModel
- Event details (name, venue, date)
- Available slots/inventory tracking
- Primary key identification

### API Endpoints

#### Authentication Endpoints
- **POST `/login`**: Authenticate and obtain JWT token
  - Request: `UserLogin` schema (email, password)
  - Response: `Token` schema (access_token, token_type)
  - No authentication required

#### User Endpoints
- **POST `/users`**: Create a new user account
  - Request: `User` schema (name, email, password, role)
  - Response: Created `UserModel`
  - No authentication required

- **GET `/users/me`**: Get current authenticated user information
  - Headers: Bearer token required
  - Response: User details with welcome message
  - Authentication required

#### Event Endpoints
- **POST `/events`**: Create a new event (Admin only)
  - Request: `Events` schema (name, venue, date, availability)
  - Response: Created `EventsModel`
  - Authentication required (Admin role)

- **GET `/events`**: Retrieve all available events
  - Response: List of `EventResponse` objects
  - No authentication required

- **POST `/events/{event_id}/book`**: Book seats for an event (User only)
  - Path Parameter: `event_id` (integer)
  - Query Parameter: `seats` (integer)
  - Response: Updated `EventBookResponse`
  - Authentication required (User role)

## Data Models

### Schemas (Pydantic)

**User** - User registration data
```python
name: str
email: str
password: str  # Max 72 characters
role: str
```

**Events** - Event creation data
```python
event_name: str
event_venue: str
event_date: datetime
event_availibility: int
```

**UserLogin** - Login credentials
```python
email: str
password: str
```

**Token** - JWT token response
```python
access_token: str
token_type: str  # "bearer"
```

## Installation

### Prerequisites
- Python 3.7+
- Docker and Docker Compose (for containerized setup) OR MySQL 5.7+ (for local setup)
- pip (Python package manager)

### Setup Option 1: Using Docker (Recommended)

1. **Clone or navigate to project directory**
```bash
cd booking-fastapi
```

2. **Start Docker containers**
```bash
docker-compose up -d
```

This will start:
- MySQL 8.0 database on port `3306`

3. **Verify MySQL is running**
```bash
docker-compose logs mysql
```

Wait for the message: `[Server] /usr/sbin/mysqld: ready for connections`

4. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

5. **Install dependencies**
```bash
pip install -r requirements.txt
```

6. **Initialize database tables**
```bash
python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### Setup Option 2: Local MySQL Installation

1. **Clone or navigate to project directory**
```bash
cd booking-fastapi
```

2. **Ensure MySQL is running**
```bash
# On Windows
net start MySQL80

# On macOS (with Homebrew)
brew services start mysql

# On Linux
sudo systemctl start mysql
```

3. **Create database and user**
```bash
mysql -u root -p
```
Then run:
```sql
CREATE DATABASE task_db;
CREATE USER 'api_user'@'localhost' IDENTIFIED BY 'api_password';
GRANT ALL PRIVILEGES ON task_db.* TO 'api_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

4. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

5. **Install dependencies**
```bash
pip install -r requirements.txt
```

6. **Initialize database tables**
```bash
python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### Post-Installation Configuration

1. **Update security settings** (IMPORTANT)
   - Edit `utils/security.py` and replace `SECRET_KEY` with a strong random string
   - Or set environment variable: `export SECRET_KEY="your-random-secret-key"`
   - Move `SECRET_KEY` to environment variables in production

2. **Optional: Create .env file for environment variables**
```bash
# Create .env file
echo "DATABASE_URL=mysql+pymysql://api_user:api_password@localhost:3306/task_db" > .env
echo "SECRET_KEY=your-very-long-random-secret-key-here" >> .env
```

## Usage

### Running the Application

```bash
# Using uvicorn
uvicorn main:app --reload

# The API will be available at http://localhost:8000
# API documentation: http://localhost:8000/docs (Swagger UI)
# Alternative docs: http://localhost:8000/redoc (ReDoc)
```

### Docker Management Commands

**Start containers:**
```bash
docker-compose up -d
```

**Stop containers:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f mysql
```

**Restart containers:**
```bash
docker-compose restart
```

**Remove volumes and start fresh:**
```bash
docker-compose down -v
docker-compose up -d
```

**View running containers:**
```bash
docker-compose ps
```

### Example API Calls

#### Create User:
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "user"
  }'
```

#### Login:
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User:
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer <your_jwt_token>"
```

#### Create Event (Admin):
```bash
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin_jwt_token>" \
  -d '{
    "event_name": "Tech Conference 2025",
    "event_venue": "Convention Center",
    "event_date": "2025-12-15T09:00:00",
    "event_availibility": 100
  }'
```

#### Get All Events:
```bash
curl -X GET "http://localhost:8000/events"
```

#### Book Event (User):
```bash
curl -X POST "http://localhost:8000/events/1/book?seats=2" \
  -H "Authorization: Bearer <user_jwt_token>"
```

## Security Considerations

1. **Password Storage**: Passwords are hashed using Argon2 and never stored in plain text
2. **Secret Key**: Keep `SECRET_KEY` confidential and store in environment variables
3. **Token Expiration**: Tokens automatically expire after 30 minutes (configurable)
4. **HTTPS**: Use HTTPS in production to protect token transmission
5. **Database Credentials**: Store database credentials in environment variables, not in code

## Configuration

### Environment Variables (Recommended)

Create a `.env` file:
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/task_db
SECRET_KEY=your-very-long-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTE=30
```

Load in application:
```python
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
```

## Database Schema

### Users Table
```sql
CREATE TABLE User (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  role VARCHAR(255)
);
```

### Events Table
```sql
CREATE TABLE Events (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  event_name VARCHAR(255),
  event_venue VARCHAR(255),
  event_date DATE,
  event_availibility INT
);
```

## Token Structure

JWT token payload includes:
- `sub`: User email (subject)
- `exp`: Token expiration time (UTC)
- `iat`: Token issued at time (UTC)
- `alg`: Algorithm (HS256)

## Dependencies

- **fastapi**: Web framework for building APIs
- **sqlalchemy**: ORM for database operations
- **pymysql**: MySQL database driver
- **passlib[argon2]**: Password hashing
- **python-jose**: JWT token handling
- **pydantic**: Data validation and serialization
- **uvicorn**: ASGI server

## Testing

Run tests with pytest:
```bash
pytest
```

## Future Enhancements

- [ ] User profile management and updates
- [ ] Event search and filtering by date/venue
- [ ] Pagination support for large event lists
- [ ] Booking history and cancellation endpoints
- [ ] Email verification for new users
- [ ] Password reset functionality
- [ ] Rate limiting to prevent abuse
- [ ] Request logging and monitoring
- [ ] API usage analytics and metrics
- [ ] Automated booking confirmation emails
- [ ] Multi-language support
- [ ] Advanced role permissions system

## Troubleshooting

### Database Connection Error
- **With Docker**: Verify MySQL container is running: `docker-compose ps`
- **Without Docker**: Verify MySQL server is running
- Check credentials in `database.py`
- Ensure database `task_db` exists
- Test connection: `mysql -u api_user -p -h localhost -D task_db`

### Docker-Specific Issues

**Port already in use:**
```bash
# Change port in docker-compose.yml
# For MySQL, change "3306:3306" to "3307:3306"
docker-compose down
docker-compose up -d
```

**MySQL won't start:**
```bash
# Check logs
docker-compose logs mysql

# Remove and restart
docker-compose down -v
docker-compose up -d
```

**Cannot connect to MySQL:**
- Ensure containers are running: `docker-compose ps`
- Check if MySQL is healthy: `docker-compose ps` (status should be "Up")
- Wait 10-15 seconds for MySQL to fully initialize
- Verify container network: `docker network ls`

### Token Validation Error
- Verify JWT token is in "Bearer <token>" format
- Check token hasn't expired
- Ensure `SECRET_KEY` matches between encoding and decoding

### Password Hashing Issues
- Install `passlib[argon2]`: `pip install passlib[argon2]`
- Ensure Argon2 is available on system

## License

MIT License - Feel free to use and modify as needed.

## Contact & Support

For issues or questions, please create an issue in the repository.
