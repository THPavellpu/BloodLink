# Bloodlink Backend

A production-ready Django REST Framework backend for a blood donor matching system with AI integration, Firebase notifications, and smart location-based donor matching.

## Features

✅ **Custom User Model** - Extended AbstractUser with blood group, location, and donation tracking
✅ **JWT Authentication** - Secure token-based authentication with SimpleJWT
✅ **Blood Request Management** - Create and manage blood donation requests
✅ **Smart Donor Matching** - Scoring-based algorithm with Haversine distance calculation
✅ **AI Integration** - Google Gemini AI for educational chatbot
✅ **Firebase Notifications** - Push notifications via FCM tokens
✅ **Database Flexibility** - Works with SQLite (dev) and PostgreSQL (production)
✅ **CORS Enabled** - Ready for Android/React Native app integration
✅ **Clean Architecture** - Modular design with separate services and serializers
✅ **Production Ready** - Gunicorn, environment variables, logging

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework
- PostgreSQL (for production on Render)

## Installation

### 1. Clone and Setup

```bash
git clone <repository-url>
cd bloodlink_backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GEMINI_API_KEY=your-gemini-api-key
FIREBASE_CREDENTIALS=/path/to/firebase-credentials.json
```

### 3. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Server runs on `http://localhost:8000`

## Database Configuration

### Development (SQLite)

Default configuration uses SQLite. No additional setup needed.

### Production (PostgreSQL)

Set `DATABASE_URL` in `.env`:

```
DATABASE_URL=postgresql://user:password@host:5432/bloodlink
```

The app automatically uses PostgreSQL when `DATABASE_URL` is set.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/login/` | Get JWT tokens |
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/token/refresh/` | Refresh access token |

### User Profile

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/profile/` | Get current user profile |
| PUT | `/api/user/update/` | Update profile |
| POST | `/api/user/location/` | Update location (lat/lon) |

### Blood Requests

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/request/create/` | Create blood request |
| GET | `/api/request/all/` | Get all active requests |
| GET | `/api/request/my_requests/` | Get user's requests |
| GET | `/api/request/{id}/` | Get specific request |
| PUT | `/api/request/{id}/update_request/` | Update request |
| DELETE | `/api/request/{id}/cancel/` | Cancel request |

### Donor Matching

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/donors/match/` | Find matching donors |

Query parameters:
- `blood_group` (required): Blood type (e.g., `A+`, `O-`)
- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate
- `limit` (optional): Max results (default: 50, max: 200)

Example:
```
GET /api/donors/match/?blood_group=A+&latitude=40.7128&longitude=-74.0060&limit=50
```

### Notifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/notifications/register_token/` | Register FCM token |
| GET | `/api/notifications/my_token/` | Get registered token |
| DELETE | `/api/notifications/deregister_token/` | Remove FCM token |

### AI Integration

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/chat/` | Chat with Gemini AI |

Request body:
```json
{
    "question": "What should I know about blood donation?",
    "context": "I want to donate blood"
}
```

## API Response Format

### Success Response

```json
{
    "message": "Operation successful",
    "data": {...}
}
```

### Error Response

```json
{
    "error": "Error message",
    "details": {...}
}
```

## Smart Donor Matching Algorithm

The matching algorithm uses a scoring system:

**Scoring Rules:**

1. **Availability** (+50 points)
   - Donor is marked as available: +50
   - Not available: 0

2. **Donation Recency** (0 to +40 points)
   - Last donation < 30 days: +0
   - Last donation 30-90 days: +20
   - Last donation > 90 days: +40
   - Never donated: +40

3. **Distance** (using Haversine formula)
   - < 5 km: +30
   - < 15 km: +20
   - ≥ 15 km: +10

**Total Score Range:** 0-100 points

Donors are ranked by score in descending order.

## Distance Calculation

The system uses the Haversine formula to calculate great-circle distances between coordinates:

```
distance = 2 * arcsin(sqrt(sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2))) * R
```

Where R = 6371 km (Earth's radius)

## Project Structure

```
bloodlink_backend/
├── config/                 # Django configuration
│   ├── settings.py        # Main settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI app
│   └── asgi.py            # ASGI app
├── users/                  # User authentication & profiles
│   ├── models.py          # CustomUser model
│   ├── views.py           # Auth views
│   ├── serializers.py     # Serializers
│   └── urls.py            # URL routing
├── requests/              # Blood requests
│   ├── models.py          # BloodRequest model
│   ├── views.py           # Request views
│   ├── serializers.py     # Serializers
│   └── urls.py            # URL routing
├── matching/              # Donor matching
│   ├── services.py        # Matching algorithm
│   ├── views.py           # Matching views
│   ├── serializers.py     # Serializers
│   └── urls.py            # URL routing
├── ai_integration/        # Gemini AI
│   ├── services.py        # Gemini service
│   ├── views.py           # AI views
│   ├── serializers.py     # Serializers
│   └── urls.py            # URL routing
├── notifications/         # Firebase FCM
│   ├── models.py          # NotificationToken model
│   ├── services.py        # FCM service
│   ├── views.py           # Notification views
│   ├── serializers.py     # Serializers
│   └── urls.py            # URL routing
├── common/                # Common utilities
│   ├── constants.py       # Constants
│   ├── exceptions.py      # Custom exceptions
│   └── permissions.py     # Custom permissions
├── manage.py              # Django management
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment
├── .env.example          # Environment template
└── README.md             # This file
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Login

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

Response:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {...}
}
```

### Using Access Token

Include in request header:
```bash
Authorization: Bearer <access_token>
```

## Deployment on Render

### 1. Prepare PostgreSQL

Create a PostgreSQL database on Render and get the connection string.

### 2. Environment Variables

Set on Render:

```
DJANGO_SETTINGS_MODULE=config.settings
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.render.com
DATABASE_URL=postgresql://...
GEMINI_API_KEY=your-key
```

### 3. Deploy

Push to GitHub, connect repository to Render, and click Deploy.

### 4. Run Migrations

After deployment, run:
```bash
python manage.py migrate
```

## Configuration & Customization

### Adding New Blood Types

Edit `users/models.py` and `requests/models.py` BLOOD_CHOICES field.

### Changing Matching Algorithm

Modify `matching/services.py` scoring rules in `calculate_donor_score()`.

### Customizing JWT Settings

Edit `config/settings.py` SIMPLE_JWT configuration.

### Adding Email Notifications

1. Configure email in `config/settings.py`
2. Create email templates
3. Add email service in `notifications/services.py`

## Development Tips

### Create Test Data

```python
python manage.py shell

from django.contrib.auth import get_user_model
User = get_user_model()

# Create a test donor
donor = User.objects.create_user(
    username='donor1',
    email='donor@example.com',
    password='testpass123',
    phone='1234567890',
    blood_group='O+',
    latitude=40.7128,
    longitude=-74.0060,
    location_name='New York',
    is_available=True
)
```

### View API Documentation in Admin

Go to `http://localhost:8000/admin/`

### Debug Mode

Set `DEBUG=True` in `.env` for detailed error messages (development only).

## Error Handling

The API returns standard HTTP status codes:

- **200** - Success
- **201** - Created
- **204** - No Content
- **400** - Bad Request
- **401** - Unauthorized
- **403** - Forbidden
- **404** - Not Found
- **500** - Server Error

## Security Considerations

✅ Passwords hashed with PBKDF2
✅ CSRF protection enabled
✅ SQL injection prevention via ORM
✅ CORS configured for specific origins
✅ JWT tokens with expiration
✅ Environment variables for secrets
✅ HTTPS recommended for production

## Testing

Create tests in each app's `tests.py` file and run:

```bash
python manage.py test
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.

## Roadmap

- [ ] Email notifications
- [ ] SMS notifications
- [ ] Donation history tracking
- [ ] Blood bank integration
- [ ] Analytics dashboard
- [ ] Social sharing
- [ ] Rating system
- [ ] Advanced search filters

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Locked

```bash
# Remove database and migrations
rm db.sqlite3
rm */migrations/0*.py

# Recreate
python manage.py makemigrations
python manage.py migrate
```

### Migration Errors

```bash
# Show migration status
python manage.py showmigrations

# Fake migration if needed
python manage.py migrate --fake app_name 0001_initial
```

## Credits

Built with Django, Django REST Framework, and Google Generative AI.
