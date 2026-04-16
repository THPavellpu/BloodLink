# Render Deployment Quick Reference

Fast troubleshooting and quick setup guide for Bloodlink backend on Render.

---

## Deployment Command Summary

```bash
# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Test locally with production settings
export DEBUG=False
python manage.py runserver --insecure

# Push to deploy
git add .
git commit -m "Deploy to Render"
git push origin main
```

---

## Render Environment Variables (Copy-Paste)

```
SECRET_KEY=GENERATE_NEW_ONE
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com,your-domain.com
DATABASE_URL=FROM_RENDER_DB
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000,http://localhost:8080
CSRF_TRUSTED_ORIGINS=https://your-frontend.com,https://your-app.onrender.com,http://localhost:3000,http://localhost:8080
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
GEMINI_API_KEY=YOUR_KEY
DJANGO_LOG_LEVEL=INFO
```

---

## Common Issues & Fixes

### 1. DisallowedHost Error
**Error**: `Invalid HTTP_HOST header: 'yourapp.onrender.com'. Forbidden host`

**Fix**: Add domain to ALLOWED_HOSTS
```
ALLOWED_HOSTS=your-app.onrender.com,your-domain.com
```

---

### 2. CORS Error from Frontend
**Error**: `Access to XMLHttpRequest has been blocked by CORS policy`

**Fix**: Add frontend URL to CORS settings
```
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000
CSRF_TRUSTED_ORIGINS=https://your-frontend.com,https://your-app.onrender.com
```

---

### 3. StaticFiles Not Found
**Error**: `404 - Static files not loading (CSS, JS)`

**Fix**: 
1. Ensure build.sh has `collectstatic`
2. Verify WhiteNoise in MIDDLEWARE
3. Check STATIC_ROOT is correct

Manually collect (from Render shell):
```bash
python manage.py collectstatic --noinput
```

---

### 4. Database Connection Error
**Error**: `Connection refused` or `password authentication failed`

**Fix**:
1. Verify DATABASE_URL is set
2. Check PostgreSQL database is created
3. Ensure credentials are correct
4. Wait for database to be ready (first deploy takes time)

Check connection locally:
```bash
# Add to terminal
export DATABASE_URL="postgresql://user:pass@host:5432/db"
python manage.py migrate
```

---

### 5. Build Fails
**Error**: `Build failed` in Render logs

**Fix**:
1. Check build.sh is executable
2. Verify requirements.txt has no syntax errors
3. Check for import errors:
   ```bash
   python -c "import django; print(django.VERSION)"
   ```
4. View full logs in Render

---

### 6. 502 Bad Gateway
**Error**: `502 Bad Gateway` after deployment

**Fix**:
1. Check logs (likely error in views or models)
2. Verify SECRET_KEY is set
3. Ensure DEBUG=False doesn't expose error details
4. Check Gunicorn is running
5. Restart service in Render dashboard

---

### 7. Migrations Not Applied
**Error**: `no such table: users_customuser`

**Fix**:
1. Ensure build.sh has: `python manage.py migrate`
2. Check for migration files locally
3. Verify DATABASE_URL is correct
4. From Render shell:
   ```bash
   python manage.py showmigrations
   python manage.py migrate
   ```

---

### 8. Can't Login / JWT Token Issues
**Error**: `401 Unauthorized` even with token

**Fix**:
1. Verify SimpleJWT is installed
2. Check SECRET_KEY matches (regeneration breaks tokens)
3. Verify token endpoint works:
   ```bash
   curl -X POST https://your-app.onrender.com/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{"username":"user","password":"pass"}'
   ```
4. Check token format: `"Authorization: Bearer <token>"`

---

## Quick Verification Checklist

After deployment visit these URLs:

```
✓ API Home: https://your-app.onrender.com/api/
✓ Admin: https://your-app.onrender.com/admin/
✓ Token: https://your-app.onrender.com/api/auth/token/ (POST)
✓ Health: https://your-app.onrender.com/api/health/ (if exists)
```

Test with curl:
```bash
# Get token
TOKEN=$(curl -s -X POST https://your-app.onrender.com/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' | jq -r '.access')

# Test authenticated endpoint
curl -H "Authorization: Bearer $TOKEN" \
  https://your-app.onrender.com/api/users/profile/
```

---

## Logs Debugging

### View Real-time Logs
```
Render Dashboard → Web Service → Logs → (auto-updates)
```

### Search Logs
1. Look for **ERROR** entries
2. Check **traceback** for exact issue
3. Find **timestamp** to correlate with requests

### Common Log Patterns
```
starting gunicorn                   → App starting
GET /api/endpoint HTTP/1.1          → Request received
200 OK                              → Request successful
404 Not Found                        → Endpoint doesn't exist
500 Server Error                    → Error in code (check traceback)
DisallowedHost exception            → Not in ALLOWED_HOSTS
CORS Error                          → Check CORS_ALLOWED_ORIGINS
```

---

## Manual Deployment Steps

If you need to manually redeploy:

1. Make code changes locally
2. Test with `python manage.py test`
3. Commit: `git add . && git commit -m "Fix issue"`
4. Push: `git push origin main`
5. Render automatically redeploys
6. Or manually in Render: Dashboard → Web Service → Manual Deploy

---

## Accessing Render Shell

Debug by running commands on Render:

1. Render Dashboard → Web Service → Connect via Shell
2. Run commands (same as local):
   ```bash
   ls -la                              # List files
   python manage.py shell              # Django shell
   python manage.py dbshell            # Database shell
   python manage.py migrate            # Run migrations
   python manage.py collectstatic      # Collect static files
   tail -f log.txt                     # View logs
   ```

---

## Environment Variables Precedence

1. Render environment variables (highest priority)
2. .env file (local testing)
3. Settings defaults (lowest priority)

To test locally:
```bash
export DEBUG=False
export ALLOWED_HOSTS=localhost
export SECRET_KEY=test-key
python manage.py runserver
```

---

## Security Reminders

⚠️ **NEVER** in Render environment:
- Hardcoded SECRET_KEY
- Database passwords
- API keys in code
- Test data with real user credentials

✓ **DO** use environment variables:
- All sensitive config in Render dashboard
- Reference with `.env.example`
- Same for local development

---

## Useful Links

- Render Django Guide: https://render.com/docs/deploy-django
- Django Settings: https://docs.djangoproject.com/en/4.2/ref/settings/
- DRF Settings: https://www.django-rest-framework.org/api-guide/settings/
- WhiteNoise Docs: http://whitenoise.evans.io/
- Gunicorn Docs: https://gunicorn.org/

---

## Contact Your Provider

If Render servers are down:
- Check status: https://status.render.com/
- Contact: https://render.com/support

---

## Advanced: Database Backup & Restore

### View Backups
```
Render → PostgreSQL → Backups
```

### Manual Backup
```bash
pg_dump $DATABASE_URL > backup.sql
```

### Restore from Backup
```
Render → PostgreSQL → Restore from Backup
```

---

## Performance Tuning

For higher traffic:

### Increase Gunicorn Workers
In Procfile:
```
web: gunicorn config.wsgi:application --workers 4 --worker-class gevent --timeout 600
```

### Enable Caching
Add to requirements.txt:
```
django-redis==5.4.0
```

Add to settings.py:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Database Connection Pooling
Add to requirements.txt:
```
psycopg2>=2.9
```

---

## Monitoring

### Email Alerts (Optional)
In Render → Notifications → Email

### Error Tracking (Optional)
Add Sentry for automatic error monitoring:
```bash
pip install sentry-sdk
```

Then configure in settings.py

---

## Notes for Next Deployment

Use this checklist each deployment cycle:

- [ ] All tests pass locally
- [ ] Code committed and pushed
- [ ] Environment variables updated
- [ ] Logs monitored after deployment
- [ ] API endpoints tested
- [ ] Frontend works with new API
- [ ] No errors in Render logs
- [ ] Database backups working

---

**Last Updated**: 2025-04-16  
**Django Version**: 4.2  
**DRF Version**: 3.14+
