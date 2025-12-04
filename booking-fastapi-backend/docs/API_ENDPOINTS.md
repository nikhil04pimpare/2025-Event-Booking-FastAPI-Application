# API Endpoints Documentation

## Base URL
```
http://localhost:8000
```

## Interactive Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Authentication Endpoints

### 1. Login (POST /login)
Authenticate user and get JWT token.

**Request:**
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- 200: Login successful
- 401: Invalid credentials

---

## User Endpoints

### 2. Register User (POST /users)
Create a new user account.

**Request:**
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "User"
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "User"
}
```

**Roles:** `Admin`, `User`, `Public`

---

### 3. Get Current User (GET /users/me)
Retrieve authenticated user information.

**Request:**
```bash
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "message": "Welcome back, John Doe! You are logged in with role: User",
  "user_id": 1,
  "email": "john@example.com"
}
```

**Status Codes:**
- 200: Success
- 401: Unauthorized (invalid/missing token)

---

## Event Endpoints

### 4. Create Event (POST /events)
Create a new event (Admin only).

**Request:**
```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -d '{
    "event_name": "Tech Conference 2025",
    "event_venue": "Convention Center",
    "event_date": "2025-12-20T10:00:00",
    "event_availibility": 100
  }'
```

**Response:**
```json
{
  "event_id": 1,
  "event_name": "Tech Conference 2025",
  "event_venue": "Convention Center",
  "event_date": "2025-12-20T10:00:00",
  "event_availibility": 100
}
```

**Status Codes:**
- 200: Event created
- 403: Forbidden (must be Admin)
- 401: Unauthorized

---

### 5. Get All Events (GET /events)
Retrieve all available events (public access).

**Request:**
```bash
curl -X GET http://localhost:8000/events
```

**Response:**
```json
[
  {
    "event_id": 1,
    "event_name": "Tech Conference 2025",
    "event_venue": "Convention Center",
    "event_date": "2025-12-20T10:00:00",
    "event_availibility": 100
  }
]
```

**Status Codes:**
- 200: Success
- 404: No events found

---

### 6. Book Event (POST /events/{event_id}/book)
Book seats for an event (User only).

**Request:**
```bash
curl -X POST "http://localhost:8000/events/1/book?seats=5" \
  -H "Authorization: Bearer USER_TOKEN"
```

**Response:**
```json
{
  "event_id": 1,
  "event_name": "Tech Conference 2025",
  "event_venue": "Convention Center",
  "event_date": "2025-12-20T10:00:00",
  "event_availibility": 95
}
```

**Status Codes:**
- 200: Booking successful
- 403: Forbidden (must be User)
- 404: Event not found
- 409: Insufficient seats available
- 401: Unauthorized

**Query Parameters:**
- `seats` (required): Number of seats to book

---

## Admin Endpoints

### 7. Get All Bookings (GET /admin/bookings)
Retrieve all booking records (Admin only).

**Request:**
```bash
curl -X GET http://localhost:8000/admin/bookings \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 2,
    "event_id": 1,
    "seats_booked": 5,
    "remaining_tickets": 95,
    "booking_time": "2025-12-04T15:30:45.123456"
  }
]
```

**Status Codes:**
- 200: Success
- 403: Forbidden (must be Admin)
- 404: No bookings found
- 401: Unauthorized

---

## Error Responses

### Standard Error Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

| Status | Detail |
|--------|--------|
| 400 | Bad Request - Invalid input format |
| 401 | Could not validate credentials |
| 403 | Not authorized to perform this action |
| 404 | Resource not found |
| 409 | Conflict - e.g., duplicate email, insufficient seats |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error |

---

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Token Structure
- **Type**: JWT (JSON Web Token)
- **Algorithm**: HS256
- **Expiration**: 30 minutes (configurable)
- **Claims**:
  - `sub`: User email
  - `exp`: Expiration timestamp
  - `iat`: Issued at timestamp

---

## User Roles

### Admin
- Create events
- View all bookings
- Cannot book events

### User
- Book events
- View own information
- Cannot create events

### Public
- View events (read-only)

---

## Testing Workflow

### 1. Create Admin User
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Admin","email":"admin@test.com","password":"123","role":"Admin"}'
```

### 2. Create Regular User
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"User","email":"user@test.com","password":"123","role":"User"}'
```

### 3. Login as Admin
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"123"}'
# Copy the access_token
```

### 4. Create Event (as Admin)
```bash
curl -X POST http://localhost:8000/events \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_name":"Concert",
    "event_venue":"Stadium",
    "event_date":"2025-12-25T18:00:00",
    "event_availibility":500
  }'
```

### 5. Login as User and Book Event
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"123"}'
# Copy the user token

curl -X POST "http://localhost:8000/events/1/book?seats=10" \
  -H "Authorization: Bearer USER_TOKEN"
```

### 6. View Bookings (as Admin)
```bash
curl -X GET http://localhost:8000/admin/bookings \
  -H "Authorization: Bearer ADMIN_TOKEN"
```
