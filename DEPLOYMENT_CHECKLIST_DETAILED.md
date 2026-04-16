# Production Deployment Checklist - Bloodlink Backend

Before deploying to Render, verify all items below are completed.

## Code Quality & Configuration

- [ ] All code committed and pushed to GitHub
- [ ] No `print()` statements left in production code (use logging instead)
- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS is properly configured
- [ ] No test data in production database
- [ ] All migrations are created and applied locally
- [ ] Settings.py has no hardcoded sensitive data

## Dependencies

- [ ] `requirements.txt` is up-to-date
- [ ] All packages have pinned versions
- [ ] Tested: `pip install -r requirements.txt` works locally
- [ ] Production packages included:
  - [ ] gunicorn
  - [ ] psycopg2-binary
  - [ ] dj-database-url
  - [ ] whitenoise
  - [ ] python-decouple
  - [ ] djangorestframework
  - [ ] djangorestframework-simplejwt
  - [ ] django-cors-headers

## Database

- [ ] PostgreSQL database created on Render
- [ ] DATABASE_URL connection string obtained
- [ ] No SQLite database committed to GitHub
- [ ] Migrations run locally and tested
- [ ] Migrations will apply successfully on fresh database

## Security

- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] CORS_ALLOWED_ORIGINS configured (not **)
- [ ] CSRF_TRUSTED_ORIGINS configured
- [ ] No API keys in settings.py or committed files
- [ ] Environment variables documented in .env.example
- [ ] SECRET_KEY is NOT the default dev key

## Static Files

- [ ] STATIC_URL = '/static/'
- [ ] STATIC_ROOT configured correctly
- [ ] WhiteNoise middleware enabled
- [ ] Build script runs collectstatic
- [ ] No static files ignored by git

## API & CORS

- [ ] CORS_ALLOWED_ORIGINS includes frontend domains
- [ ] CSRF_TRUSTED_ORIGINS includes all domains
- [ ] JWT authentication working locally
- [ ] API endpoints tested with Postman/insomnia
- [ ] Error responses formatted correctly

## Build & Deployment Files

- [ ] Procfile exists and correct:
  ```
  web: gunicorn config.wsgi:application --log-file -
  ```
- [ ] build.sh is executable and correct:
  - [ ] Updates pip
  - [ ] Installs requirements
  - [ ] Runs collectstatic
  - [ ] Runs migrations
- [ ] .gitignore excludes:
  - [ ] .env
  - [ ] db.sqlite3
  - [ ] staticfiles/
  - [ ] __pycache__/
  - [ ] *.pyc
  - [ ] venv/
  - [ ] Firebase credentials

## Logging & Monitoring

- [ ] Logging configuration in settings.py
- [ ] Django logs to stderr (for Render logs)
- [ ] DJANGO_LOG_LEVEL set (likely INFO or WARNING)
- [ ] No sensitive data logged
- [ ] Error handling implemented

## Render Setup

- [ ] GitHub repository created and pushed
- [ ] Render account created
- [ ] PostgreSQL database provisioned
- [ ] Web Service connected to GitHub repo
- [ ] Build command set to: `./build.sh`
- [ ] Start command set to: `gunicorn config.wsgi:application`

## Environment Variables (in Render)

- [ ] SECRET_KEY - strong random value
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS - your render domain
- [ ] DATABASE_URL - from PostgreSQL database
- [ ] CORS_ALLOWED_ORIGINS - frontend domains
- [ ] CSRF_TRUSTED_ORIGINS - frontend + API domains
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] GEMINI_API_KEY (if using AI features)
- [ ] DJANGO_LOG_LEVEL = INFO

## Pre-Deployment Testing (Local)

- [ ] Test with: `python manage.py runserver`
- [ ] Test admin: `http://localhost:8000/admin/`
- [ ] Test API endpoints:
  - [ ] POST /api/auth/token/ (login)
  - [ ] GET /api/users/profile/ (requires auth)
  - [ ] Test at least one main endpoint
- [ ] Test CORS by calling from frontend
- [ ] Test with ALLOWED_HOSTS restricted
- [ ] Test with DEBUG = False locally

## Post-Deployment Verification

After deploying to Render:

- [ ] Visit API home: `https://bloodlink-api.onrender.com/api/`
- [ ] Test health endpoint
- [ ] Test token generation
- [ ] Test authenticated endpoint
- [ ] Check logs for errors
- [ ] Test from Android app
- [ ] Verify HTTPS working
- [ ] Check static files loading (if applicable)

## Optional - Additional Security

- [ ] Add Sentry for error tracking
- [ ] Enable database backups
- [ ] Configure email for error notifications
- [ ] Add rate limiting to API
- [ ] Implement request logging
- [ ] Add API documentation (Swagger/Redoc)
- [ ] Enable GZIP compression

## Documentation

- [ ] README.md updated with deployment info
- [ ] API endpoints documented
- [ ] Environment variables documented (.env.example updated)
- [ ] Deployment notes added (RENDER_DEPLOYMENT_GUIDE.md)
- [ ] Build script documented

## Final Steps

1. Create backup of local database
2. Commit all changes with message: "Prepare for Render production deployment"
3. Push to GitHub
4. Verify Render deployment completes
5. Test all critical endpoints
6. Monitor logs for errors
7. Inform Android app team of new API URL

---

**Deployment Date: ___________**
**Deployed By: ___________**
**Status: [ ] Production Ready [ ] Reverted [ ] Hotfix Applied**
