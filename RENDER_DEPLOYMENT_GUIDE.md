# Bloodlink Backend - Render Deployment Guide

Complete guide to deploy your Django REST Framework backend to Render with PostgreSQL.

## Prerequisites

- Render account (https://render.com)
- GitHub repository with your code pushed
- PostgreSQL database created on Render
- Gemini API key (optional for AI features)

---

## Step 1: Prepare Your Repository

Ensure all changes are committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

---

## Step 2: Set Up PostgreSQL Database on Render

1. Log in to Render dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `bloodlink-db` (or your preference)
   - **Database**: `bloodlink_db`
   - **User**: `bloodlink_user` (or your preference)
   - **Region**: Choose closest to your users
4. Create the database and copy the connection URI
   - It will look like: `postgresql://user:password@host:5432/dbname`
   - Save this for Step 4

---

## Step 3: Create Web Service on Render

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `bloodlink-api` (or your preference)
   - **Environment**: `Python 3`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: Leave empty (if project is at repo root)
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`

---

## Step 4: Set Environment Variables

In Render, go to your Web Service → Environment:

Add the following variables:

```env
# Core Django Settings
SECRET_KEY=<generate-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=bloodlink-api.onrender.com,<your-domain-if-any>

# Database (Render provides this automatically during database creation)
DATABASE_URL=<copy-from-postgresql-database>

# CORS & Security
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://localhost:8080,https://your-frontend-domain.com,https://bloodlink-api.onrender.com

# SSL/HTTPS (Render handles SSL automatically)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# API Keys
GEMINI_API_KEY=<your-gemini-api-key>

# Logging
DJANGO_LOG_LEVEL=INFO
```

### Generate SECRET_KEY

Run this locally and copy the output:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Step 5: Deploy

1. Save environment variables in Render
2. Render will automatically:
   - Pull your code
   - Run `./build.sh` (installs dependencies, collects static files, runs migrations)
   - Start the web service with gunicorn

3. Monitor deployment in Render logs
4. Visit `https://bloodlink-api.onrender.com` to verify

---

## Step 6: Verify Deployment

### Test API Health

```bash
curl https://bloodlink-api.onrender.com/api/healthz/
```

### Check Logs

Go to your Render Web Service → Logs to view deployment and runtime logs.

### Test Endpoints

1. Admin Panel: `https://bloodlink-api.onrender.com/admin/`
2. API Root: `https://bloodlink-api.onrender.com/api/`
3. Token Endpoint: `https://bloodlink-api.onrender.com/api/auth/token/`

---

## Step 7: Configure Android App

Update your Android app's API base URL:

```
https://bloodlink-api.onrender.com/api/
```

Ensure your app sends:
- `Authorization: Bearer <access_token>` for authenticated requests
- `Content-Type: application/json` for POST/PUT requests

---

## Updating Your Application

Every time you push to `main`:

1. Render automatically pulls changes
2. Runs build.sh script
3. Restarts the service

To manually trigger a redeploy:
- In Render dashboard → Web Service → "Manual Deploy"

---

## Production Security Checklist

- [ ] `DEBUG=False` in production environment
- [ ] `SECRET_KEY` is strong and random
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] `CORS_ALLOWED_ORIGINS` restricts to your frontend domains
- [ ] `CSRF_TRUSTED_ORIGINS` is configured
- [ ] SSL/HTTPS is enabled (Render handles this)
- [ ] Database credentials are secure
- [ ] API keys are in environment variables (not hardcoded)
- [ ] Logs are monitored for errors
- [ ] Database backups are enabled (Render auto-backup)

---

## Troubleshooting

### Issue: Build fails with "No module named..."
**Solution**: Ensure package is in `requirements.txt` and push changes

### Issue: "DisallowedHost" error
**Solution**: Add your domain to `ALLOWED_HOSTS` environment variable

### Issue: Static files not loading
**Solution**: WhiteNoise middleware is configured. Run `collectstatic` manually if needed:
```bash
python manage.py collectstatic --noinput
```

### Issue: Database connection error
**Solution**: Verify `DATABASE_URL` environment variable is set correctly

### Issue: CORS errors from frontend
**Solution**: Add your frontend URL to `CORS_ALLOWED_ORIGINS` environment variable

### Issue: 502 Bad Gateway
**Solution**: 
1. Check Render logs for errors
2. Ensure `gunicorn` is running
3. Verify database connection

---

## Monitoring & Maintenance

### Enable Error Tracking
Add Sentry for error monitoring:

1. Create Sentry account (https://sentry.io)
2. Add to `requirements.txt`:
   ```
   sentry-sdk==1.50.1
   ```
3. Add to `config/settings.py`:
   ```python
   import sentry_sdk
   
   sentry_sdk.init(
       dsn=config('SENTRY_DSN', default=''),
       traces_sample_rate=0.1,
       environment=config('ENVIRONMENT', default='production'),
   )
   ```
4. Add `SENTRY_DSN` to Render environment variables

### Database Backups
- Render automatically backs up PostgreSQL databases
- View in Render dashboard → PostgreSQL Database → Backups

### View Logs
- Real-time logs: Render dashboard → Web Service → Logs
- Filter by "Error" or "Warning" to troubleshoot

---

## Scaling & Performance

### Optimize for Production:

1. **Gunicorn Workers**: Update start command to:
   ```
   gunicorn config.wsgi:application --workers 4 --worker-class=sync
   ```

2. **Database Connection Pooling**: Add to `requirements.txt`:
   ```
   dj-database-url[postgresql]
   ```

3. **Caching**: Consider adding Redis for session/cache:
   - Add `django-redis==5.4.0` to `requirements.txt`
   - Configure in `settings.py`

4. **CDN for Static Files**: Use Render's CDN or integrate Cloudflare

---

## Next Steps

1. Test all API endpoints from Android app
2. Monitor logs for errors
3. Set up Sentry for error tracking
4. Configure email notifications (optional)
5. Performance testing with realistic load

---

## Support

For Render support: https://render.com/docs
For Django deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
For DRF API: https://www.django-rest-framework.org/
