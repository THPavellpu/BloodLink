# Bloodlink Backend - Complete Setup Guide

## What's Included

✅ Django 4.2 with REST Framework
✅ Custom User Model with blood donor fields
✅ JWT Authentication with SimpleJWT
✅ Blood Request Management System
✅ Smart Donor Matching with Haversine Distance Calculation
✅ Google Gemini AI Integration
✅ Firebase Cloud Messaging (FCM) Notification System
✅ SQLite for Development / PostgreSQL for Production
✅ CORS Configuration for Mobile Apps
✅ Clean Architecture with Modular Design
✅ Production-Ready with Gunicorn & WhiteNoise
✅ Comprehensive API Documentation

## Quick Start (5 minutes)

### 1. Initial Setup

```bash
# Navigate to project
cd bloodlink_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# For development, mostly defaults are fine
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser

# Create sample data (optional)
python create_sample_data.py
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

## Testing the API

### Using cURL

#### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "name": "Test User",
    "phone": "1234567890",
    "blood_group": "O+",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "location_name": "New York"
  }'
```

#### 2. Login

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

Save the `access` token from response.

#### 3. Get Your Profile

```bash
curl -X GET http://localhost:8000/api/user/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. Find Donor Matches

```bash
curl -X GET "http://localhost:8000/api/donors/match/?blood_group=O%2B&latitude=40.7128&longitude=-74.0060" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 5. Create Blood Request

```bash
curl -X POST http://localhost:8000/api/request/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "blood_group": "O+",
    "latitude": 40.7480,
    "longitude": -73.9862,
    "location_name": "Midtown NYC",
    "urgency": "High",
    "message": "Emergency blood needed"
  }'
```

### Using Django Admin

1. Go to `http://localhost:8000/admin/`
2. Log in with superuser credentials
3. Create/manage users, blood requests, tokens

## Project Structure Overview

```
bloodlink_backend/
│
├── config/                      # Django configuration
│   ├── settings.py             # All settings (dev & prod)
│   ├── urls.py                 # URL routing
│   ├── wsgi.py & asgi.py       # Application entrypoints
│
├── users/                       # User authentication
│   ├── models.py               # CustomUser model
│   ├── views.py                # Auth & profile views
│   ├── serializers.py          # Validation & serialization
│   ├── urls.py                 # User routes
│
├── requests/                    # Blood requests
│   ├── models.py               # BloodRequest model
│   ├── views.py                # Request management
│   ├── serializers.py          # Validation
│   ├── urls.py                 # Request routes
│
├── matching/                    # Donor matching algorithm
│   ├── services.py             # Haversine & scoring
│   ├── views.py                # Matching endpoints
│   ├── serializers.py          # Match serialization
│   ├── urls.py                 # Matching routes
│
├── ai_integration/              # Gemini AI
│   ├── services.py             # AI service & prompts
│   ├── views.py                # Chat endpoint
│   ├── serializers.py          # Query/response formatting
│   ├── urls.py                 # AI routes
│
├── notifications/              # Firebase FCM
│   ├── models.py               # Token storage
│   ├── services.py             # FCM sender
│   ├── views.py                # Token management
│   ├── serializers.py          # Token validation
│   ├── urls.py                 # Notification routes
│
├── common/                      # Shared utilities
│   ├── constants.py            # Constants
│   ├── exceptions.py           # Custom exceptions
│   ├── permissions.py          # Custom permissions
│
├── manage.py                   # Django CLI
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment
├── build.sh                    # Build script
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── README.md                   # Full documentation
├── DEPLOYMENT.md               # Deployment guide
├── API_TESTING_GUIDE.txt       # cURL examples
└── ENDPOINTS.txt               # Quick endpoint reference
```

## Core Models

### CustomUser
- Extended Django User with blood donor fields
- Fields: name, phone, blood_group, latitude, longitude, location_name, is_available, last_donation_date

### BloodRequest
- Represents a blood request/need
- Fields: user, blood_group, location, urgency, message, is_fulfilled

### NotificationToken
- Stores FCM tokens for push notifications
- Enables targeted notifications to matching donors

## Algorithms & Features

### Smart Donor Matching

Scoring-based ranking system:

```
Availability Score:        +50 if available
Donation Recency:
  <30 days:               +0
  30-90 days:            +20
  >90 days:              +40
  Never donated:         +40
Distance (Haversine):
  <5 km:                 +30
  <15 km:                +20
  ≥15 km:                +10
TOTAL RANGE:             0-100 points
```

### Haversine Distance Formula

Calculates great-circle distance between coordinates:

```
d = 2 * arcsin(sqrt(sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2))) * R

R = 6371 km (Earth's radius)
```

## Authentication Flow

1. **Register** → POST `/api/auth/register/`
2. **Login** → POST `/api/login/` (receive access + refresh tokens)
3. **Request API** → Include `Authorization: Bearer <access_token>` header
4. **Token Expired** → POST `/api/token/refresh/` with refresh token

## Database Configuration

### Development (Default - SQLite)
No setup needed. Database file: `db.sqlite3`

### Production (PostgreSQL)

Set `DATABASE_URL` environment variable:

```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

The app automatically switches to PostgreSQL when this variable is set.

## Environment Variables

Create `.env` file with:

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True  # False in production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
# DATABASE_URL=postgresql://...  (only for production)

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# AI
GEMINI_API_KEY=your-gemini-api-key

# Firebase (Optional)
FIREBASE_CREDENTIALS=/path/to/service-account.json
```

## Deployment to Render

### Prerequisites
- GitHub account with pushed code
- PostgreSQL database on Render
- Gemini API key

### Steps

1. **Create PostgreSQL Database**
   - Visit render.com
   - Create PostgreSQL service
   - Copy connection string

2. **Create Web Service**
   - Connect GitHub repository
   - Select Python 3.11
   - Set environment variables:
     ```
     SECRET_KEY=<new-random-key>
     DEBUG=False
     ALLOWED_HOSTS=yourdomain.render.com
     DATABASE_URL=<postgres-connection-string>
     GEMINI_API_KEY=<api-key>
     CORS_ALLOWED_ORIGINS=https://yourdomain.render.com
     ```

3. **Configure Build**
   - Build Command: `pip install -r requirements.txt && python manage.py migrate`
   - Start Command: `gunicorn config.wsgi --log-file -`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Test API endpoints

## Common Commands

```bash
# Start development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Make database migration
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Create sample data
python create_sample_data.py

# Run tests
python manage.py test

# Open Django shell
python manage.py shell

# Collect static files (production)
python manage.py collectstatic --no-input

# Check for issues
python manage.py check

# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register user |
| POST | `/api/login/` | Login (get tokens) |
| POST | `/api/token/refresh/` | Refresh access token |
| GET | `/api/user/profile/` | Get profile |
| PUT | `/api/user/update/` | Update profile |
| POST | `/api/user/location/` | Update location |
| POST | `/api/request/create/` | Create blood request |
| GET | `/api/request/all/` | Get all requests |
| GET | `/api/request/my_requests/` | Get my requests |
| GET | `/api/request/{id}/` | Get request details |
| PUT | `/api/request/{id}/update_request/` | Update request |
| DELETE | `/api/request/{id}/cancel/` | Cancel request |
| GET | `/api/donors/match/` | Find matching donors |
| POST | `/api/notifications/register_token/` | Register FCM token |
| GET | `/api/notifications/my_token/` | Get my FCM token |
| DELETE | `/api/notifications/deregister_token/` | Remove FCM token |
| POST | `/api/ai/chat/` | Chat with AI |
| GET | `/admin/` | Django admin panel |

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

### Module Not Found
```bash
# Reactivate environment and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

### Database Locked
```bash
# Remove and recreate database
rm db.sqlite3
python manage.py migrate
```

### Migration Errors
```bash
# Show migration status
python manage.py showmigrations

# Clear and start fresh (development only!)
rm db.sqlite3
rm */migrations/000*.py
python manage.py migrate
```

## Security Best Practices

✅ Passwords hashed with PBKDF2
✅ CSRF tokens on all forms
✅ SQL injection prevention via ORM
✅ CORS restricted to known origins
✅ JWT tokens with expiration
✅ Environment variables for secrets
✅ HTTPS recommended for production
✅ Rate limiting (can be added)
✅ Input validation on all endpoints

## Performance Optimizations

- Database indexing on frequently queried fields
- Select_related for foreign keys
- Pagination on list endpoints
- JWT caching
- Static file compression

## Next Steps

1. ✅ Install and run locally
2. ✅ Test all endpoints
3. ✅ Create your own users and data
4. ✅ Deploy to Render
5. ✅ Connect Android/React app
6. ✅ Monitor and maintain

## Support & Documentation

- Full README: See `README.md`
- API Testing Guide: See `API_TESTING_GUIDE.txt`
- Deployment Guide: See `DEPLOYMENT.md`
- Endpoints Quick Ref: See `ENDPOINTS.txt`

## License

MIT License - See LICENSE file

Happy coding! 🩸💻
