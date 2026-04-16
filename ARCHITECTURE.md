# Bloodlink Backend - Architecture & Design Document

## System Overview

Bloodlink Backend is a production-ready Django REST API for a blood donor matching platform. It uses clean architecture principles with modular, service-oriented design.

## Architecture Layers

```
┌─────────────────────────────────────────┐
│         DRF ViewSets & Routers          │  Presentation Layer
├─────────────────────────────────────────┤
│      Serializers & Validators           │  Validation Layer
├─────────────────────────────────────────┤
│    Services & Business Logic            │  Business Logic Layer
├─────────────────────────────────────────┤
│      Django ORM Models                  │  Data Access Layer
├─────────────────────────────────────────┤
│      SQLite / PostgreSQL                │  Persistence Layer
└─────────────────────────────────────────┘
```

## Module Breakdown

### 1. Users Module (`users/`)

**Purpose:** User authentication and profile management

**Components:**
- **Model** (`CustomUser`): Extends Django AbstractUser with blood donor fields
- **Serializers**: 
  - `UserSerializer`: Full user representation
  - `UserRegistrationSerializer`: Registration validation
  - `CustomTokenObtainPairSerializer`: Enhanced JWT with user data
  - `UserUpdateSerializer`: Profile update validation
  - `LocationUpdateSerializer`: Location validation
- **Views**: 
  - `CustomTokenObtainPairView`: JWT token endpoint
  - `AuthViewSet`: Registration endpoint
  - `UserViewSet`: Profile, update, location endpoints

**Database Schema:**
```sql
CustomUser extends AbstractUser
├── phone (CharField, unique)
├── blood_group (CharField, choices)
├── latitude (FloatField)
├── longitude (FloatField)
├── location_name (CharField)
├── is_available (BooleanField)
├── last_donation_date (DateField, nullable)
├── created_at (DateTimeField, auto_now_add)
└── updated_at (DateTimeField, auto_now)
```

**Endpoints:**
- POST `/api/auth/register/` - Register new user
- POST `/api/login/` - Get JWT tokens
- GET `/api/user/profile/` - Get current user profile
- PUT `/api/user/update/` - Update profile
- POST `/api/user/location/` - Update location

---

### 2. Requests Module (`requests/`)

**Purpose:** Blood request lifecycle management

**Components:**
- **Model** (`BloodRequest`): Blood donation request with urgency levels
- **Serializers**:
  - `BloodRequestSerializer`: Full request representation
  - `BloodRequestCreateSerializer`: Validation on creation
  - `BloodRequestUpdateSerializer`: Partial update validation
- **Views**: `BloodRequestViewSet` - CRUD operations

**Database Schema:**
```sql
BloodRequest
├── user (ForeignKey to CustomUser)
├── blood_group (CharField, choices)
├── latitude (FloatField)
├── longitude (FloatField)
├── location_name (CharField)
├── urgency (CharField, choices: Low/Medium/High)
├── message (TextField)
├── is_fulfilled (BooleanField)
├── created_at (DateTimeField, auto_now_add)
└── updated_at (DateTimeField, auto_now)
```

**Endpoints:**
- POST `/api/request/create/` - Create new request
- GET `/api/request/all/` - Get all active requests
- GET `/api/request/my_requests/` - Get user's requests
- GET `/api/request/{id}/` - Get request details
- PUT `/api/request/{id}/update_request/` - Update request
- DELETE `/api/request/{id}/cancel/` - Cancel request

---

### 3. Matching Module (`matching/`)

**Purpose:** Smart donor-to-request matching algorithm

**Components:**
- **Services** (`matching/services.py`):
  - `haversine_distance()`: Calculate distance between coordinates
  - `calculate_donor_score()`: Score individual donor
  - `find_matching_donors()`: Rank donors by score
- **Serializers**:
  - `DonorMatchSerializer`: Matched donor with score
  - `BloodMatchQuerySerializer`: Query parameter validation
- **Views**: `DonorMatchingViewSet` - Matching endpoint

**Matching Algorithm:**

```
Score Calculation:
  Availability:     if available +50, else 0
  Recency:          
    < 30d → +0,
    30-90d → +20,
    > 90d → +40,
    never → +40
  Distance (Haversine):
    < 5km → +30,
    < 15km → +20,
    ≥ 15km → +10
  
  Total: 0-100 points
  
Ranking: Descending by total score
```

**Haversine Formula:**
```
d = 2 * arcsin(sqrt(sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2))) * R
R = 6371 km (Earth's radius)
```

**Endpoints:**
- GET `/api/donors/match/` - Find matching donors

**Query Parameters:**
- `blood_group` (required): Blood type
- `latitude` (required): Request latitude
- `longitude` (required): Request longitude
- `limit` (optional): Max results (default: 50, max: 200)

**Response:**
```json
{
  "blood_group": "A+",
  "request_location": {"latitude": 40.7128, "longitude": -74.0060},
  "total_matches": 15,
  "donors": [
    {
      "donor": {...user data...},
      "score": 85,
      "distance": 3.2
    },
    ...
  ]
}
```

---

### 4. AI Integration Module (`ai_integration/`)

**Purpose:** Gemini AI integration for blood donation chatbot

**Components:**
- **Services** (`ai_integration/services.py`):
  - `GeminiAIService`: Wrapper around Google Generative AI
  - `gemini_service`: Singleton instance
- **Serializers**:
  - `AIQuerySerializer`: Question and context validation
  - `AIResponseSerializer`: Response formatting
- **Views**: `AIIntegrationViewSet` - Chat endpoint

**Features:**
- Graceful error handling if API key missing
- Context-aware responses about blood donation
- Fallback responses if service unavailable

**Endpoints:**
- POST `/api/ai/chat/` - Chat query

**Request:**
```json
{
  "question": "What are the eligibility requirements to donate blood?",
  "context": "I want to donate blood for the first time"
}
```

**Response:**
```json
{
  "success": true,
  "answer": "To donate blood, you must...",
  "model": "gemini-pro"
}
```

---

### 5. Notifications Module (`notifications/`)

**Purpose:** Firebase Cloud Messaging for push notifications

**Components:**
- **Model** (`NotificationToken`): Stores FCM tokens per user
- **Services** (`notifications/services.py`):
  - `FCMService`: Firebase integration wrapper
  - `fcm_service`: Singleton instance
- **Serializers**:
  - `NotificationTokenSerializer`: Token representation
  - `FCMTokenRegisterSerializer`: Token registration
- **Views**: `NotificationViewSet` - Token management

**Database Schema:**
```sql
NotificationToken (OneToOneField to CustomUser)
├── user (OneToOneField)
├── token (TextField)
├── created_at (DateTimeField, auto_now_add)
└── updated_at (DateTimeField, auto_now)
```

**Features:**
- Single token per user (OneToOne relationship)
- Single and multicast notifications
- Graceful handling if Firebase not configured

**Endpoints:**
- POST `/api/notifications/register_token/` - Register FCM token
- GET `/api/notifications/my_token/` - Get registered token
- DELETE `/api/notifications/deregister_token/` - Remove token

---

### 6. Common Module (`common/`)

**Purpose:** Shared utilities, constants, and helpers

**Components:**
- **Constants** (`common/constants.py`):
  - Blood type lists
  - Urgency levels
  - Distance filters
  - Donation recency thresholds
- **Exceptions** (`common/exceptions.py`):
  - Custom API exceptions
- **Permissions** (`common/permissions.py`):
  - Custom permission classes

---

## Data Flow Diagrams

### Authentication Flow
```
User Registration
    ↓
UserRegistrationSerializer validation
    ↓
CustomUser.objects.create_user()
    ↓
Auth token pair response
```

### Blood Request & Matching Flow
```
User creates BloodRequest
    ↓
BloodRequestCreateSerializer validation
    ↓
BloodRequest stored in database
    ↓
User queries /api/donors/match/
    ↓
find_matching_donors() executes:
  1. Query donors with blood_group + is_available=True
  2. For each donor, calculate_donor_score():
     - Haversine distance from request location
     - Score based on availability, recency, distance
  3. Sort by score descending
    ↓
Return ranked donors with scores
```

### Notification Flow
```
1. User registers FCM token via /api/notifications/register_token/
   ↓
2. NotificationToken stored in database
   ↓
3. When blood request created:
   - Find matching donors
   - Get their FCM tokens
   - Send push notification via Firebase
   ↓
4. Android app receives notification
```

---

## Database Design

### Entity Relationship Diagram

```
CustomUser (1) ──→ (M) BloodRequest
   ↓
   └──→ (1) NotificationToken

Relationships:
- User has many BloodRequests (ForeignKey)
- User has one NotificationToken (OneToOneField)
- BloodRequest belongs to one User (ForeignKey)
```

### Indexes

```sql
-- For performance optimization
CREATE INDEX idx_user_blood_group ON users_customuser(blood_group);
CREATE INDEX idx_user_is_available ON users_customuser(is_available);
CREATE INDEX idx_request_blood_group ON requests_bloodrequest(blood_group);
CREATE INDEX idx_request_user ON requests_bloodrequest(user_id);
CREATE INDEX idx_token_user ON notifications_notificationtoken(user_id);
```

---

## API Security

### Authentication
- JWT tokens with SimpleJWT
- Access token lifetime: 24 hours
- Refresh token lifetime: 7 days
- Tokens signed with Django SECRET_KEY

### Authorization
- IsAuthenticated permission on all endpoints (except registration/login)
- Ownership checks for user resources
- Admin panel at `/admin/`

### CORS
- Configurable allowed origins
- Credentials allowed
- Android app whitelist

### Input Validation
- Serializer validation on all inputs
- Type validation for coordinates
- Blood group enum validation
- Distance range validation

### SQL Injection Protection
- Django ORM (no raw SQL queries)
- Parameterized queries

### CSRF Protection
- CSRF middleware enabled
- CSRF tokens for form submissions

---

## Error Handling

### Response Format

**Success (2xx):**
```json
{
  "message": "Operation successful",
  "data": {...}
}
```

**Error (4xx/5xx):**
```json
{
  "error": "Error message",
  "details": {...}
}
```

### Status Codes
- 200: OK
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

---

## Deployment Architecture

### Development
```
Django Development Server (runserver)
    ↓
SQLite Database
    ↓
Static files (collected locally)
```

### Production (Render)
```
Django + Gunicorn (Web Service)
    ↓
PostgreSQL (Database Service)
    ↓
Static files (WhiteNoise middleware)
    ↓
Environment variables (Render config)
```

### Configuration Management

**Environment-based:**
- DEBUG flag
- ALLOWED_HOSTS
- CORS_ALLOWED_ORIGINS
- DATABASE_URL switching

**Feature flags:**
- Gemini API availability
- Firebase availability

---

## Performance Considerations

### Database Optimization
- Foreign key indexing
- Blood group + availability indexes
- Pagination (20 items/page default)
- Select_related for joins

### Query Optimization
```python
# Good: Select related
donors = User.objects.select_related('fcm_token').filter(...)

# Avoid: N+1 queries
for donor in User.objects.all():
    print(donor.blood_group)  # Extra query each time
```

### Caching (Can be added)
- JWT token blacklist cache
- QuerySet caching for matching

### Rate Limiting (Can be added)
- Per-user request limits
- Per-endpoint throttling

---

## Testing Strategy

### Unit Tests
```python
# models/tests.py
- Test CustomUser creation
- Test blood group validation
- Test location validation

# serializers/tests.py
- Test validation rules
- Test error messages

# services/tests.py
- Test Haversine distance calculation
- Test donor scoring algorithm
```

### Integration Tests
```python
- Test authentication flow
- Test blood request lifecycle
- Test matching algorithm
- Test API endpoints
```

### Test Coverage
- Aim for >80% coverage
- Test edge cases
- Test error scenarios

---

## Key Design Patterns

### 1. Service Layer Pattern
```python
# services.py contains business logic
# views.py calls service functions
# Separation of concerns
```

### 2. Serializer Pattern
```python
# Input validation via serializers
# Output formatting via serializers
# DRF convention
```

### 3. ViewSet Pattern
```python
# Actions for custom endpoints
# Router for URL generation
# DRF convention
```

### 4. Singleton Pattern
```python
# gemini_service = GeminiAIService()
# fcm_service = FCMService()
# Reused across requests
```

### 5. Factory Pattern
```python
# get_user_model()
# Flexible User model reference
# Django convention
```

---

## Future Enhancements

### Short Term
- [ ] Email notifications
- [ ] Donation history tracking
- [ ] Donor ratings/reviews
- [ ] Advanced search filters

### Medium Term
- [ ] Appointment booking
- [ ] Blood bank integration
- [ ] SMS notifications
- [ ] Analytics dashboard
- [ ] Social features

### Long Term
- [ ] Mobile app (native)
- [ ] Real-time updates (WebSockets)
- [ ] ML-based recommendations
- [ ] Health metrics integration

---

## Monitoring & Logging

### Logging Configuration
- Console logging in development
- File/cloud logging in production
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Monitoring
- Error tracking (Sentry)
- Uptime monitoring (UptimeRobot)
- Performance monitoring (New Relic)
- Database monitoring (Render dashboard)

### Metrics to Track
- API response times
- Error rates
- Database query times
- User sign-ups
- Blood requests resolved

---

## Maintenance

### Regular Tasks
- Review logs weekly
- Update dependencies monthly
- Security audit quarterly
- Database backup verification
- Performance tuning as needed

### Upgrade Path
- Django LTS version tracking
- DRF version updates
- Security patch application
- Python version compatibility

---

## Conclusion

This architecture provides:
✅ Clean separation of concerns
✅ Scalable modular design
✅ Production-ready deployment
✅ Security best practices
✅ Easy maintenance and testing
✅ Future enhancement flexibility

The system is ready for production deployment and can handle significant user load with proper infrastructure scaling.
