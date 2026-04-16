# DEPLOYMENT_CHECKLIST.md

## Quick Start Checklist

### Development Setup
- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Create sample data: `python create_sample_data.py`
- [ ] Start server: `python manage.py runserver`

### Testing
- [ ] Test authentication endpoints
- [ ] Test user profile endpoints
- [ ] Test blood request CRUD
- [ ] Test donor matching algorithm
- [ ] Test notifications
- [ ] Test AI chat (if API key set)

### Production Deployment on Render

#### Step 1: Prepare Repository
- [ ] Push code to GitHub
- [ ] Ensure `.gitignore` excludes `.env` and `db.sqlite3`
- [ ] Include `requirements.txt`
- [ ] Include `Procfile`

#### Step 2: Set Up PostgreSQL
- [ ] Create PostgreSQL database on Render
- [ ] Copy connection string

#### Step 3: Create Web Service on Render
- [ ] Connect GitHub repository
- [ ] Select Python 3.11+ runtime
- [ ] Set environment variables:
  ```
  SECRET_KEY=<generate-new-key>
  DEBUG=False
  ALLOWED_HOSTS=yourdomain.render.com
  DATABASE_URL=<from-postgres-database>
  GEMINI_API_KEY=<your-api-key>
  CORS_ALLOWED_ORIGINS=https://yourdomain.render.com,https://yourapp.com
  ```

#### Step 4: Configure Build Settings
- [ ] Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input`
- [ ] Start Command: `gunicorn config.wsgi --log-file -`

#### Step 5: Deploy
- [ ] Click "Create Web Service"
- [ ] Monitor deployment logs
- [ ] Verify API is responding

#### Step 6: Post-Deployment
- [ ] Test all endpoints on production
- [ ] Create admin user
- [ ] Verify CORS headers
- [ ] Check JWT token flow
- [ ] Set up monitoring

## Environment Variables for Production

```
# Django Configuration
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.render.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://username:password@host:5432/dbname

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.render.com,https://yourapp.com

# AI Integration
GEMINI_API_KEY=your-gemini-api-key

# Firebase (optional)
FIREBASE_CREDENTIALS=/path/to/credentials.json

# Security (optional)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Monitoring & Maintenance

- [ ] Set up error logging (Sentry)
- [ ] Set up uptime monitoring
- [ ] Configure backup schedules
- [ ] Monitor database performance
- [ ] Review logs regularly
- [ ] Update dependencies quarterly

## Common Issues & Solutions

### Issue: Database Connection Failed
- Solution: Verify DATABASE_URL is correct
- Check PostgreSQL service is running

### Issue: Static Files Not Served
- Solution: Run `python manage.py collectstatic`
- Update static file configuration

### Issue: CORS Errors
- Solution: Verify CORS_ALLOWED_ORIGINS includes your app domain
- Check requests have proper Origin header

### Issue: JWT Token Issues
- Solution: Verify SECRET_KEY is same across all instances
- Check token expiration settings

## Security Checklist

- [ ] SECRET_KEY is strong and unique
- [ ] DEBUG is False in production
- [ ] HTTPS is enforced
- [ ] CORS is restricted to known origins
- [ ] Database credentials in environment variables
- [ ] API keys not in source code
- [ ] Regular security updates
- [ ] SQL injection prevention (using ORM)
- [ ] CSRF protection enabled
- [ ] XSS protection headers set
