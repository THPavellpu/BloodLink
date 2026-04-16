"""
Production settings checklist for Django deployment.

Before deploying to production:

1. SECRET KEY
   - Generate a new SECRET_KEY
   - Command: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

2. DEBUG
   - Set DEBUG=False in environment

3. ALLOWED_HOSTS
   - Add your domain names
   - Format: domain.com,www.domain.com

4. CORS
   - Configure CORS_ALLOWED_ORIGINS for your app URL
   - Remove localhost entries

5. SSL/HTTPS
   - Use HTTPS only
   - Set SECURE_SSL_REDIRECT=True

6. SECURITY HEADERS
   - SECURE_BROWSER_XSS_FILTER=True
   - SECURE_CONTENT_SECURITY_POLICY
   - X_FRAME_OPTIONS='DENY'

7. DATABASE
   - Use PostgreSQL (not SQLite)
   - Use DATABASE_URL from Render

8. GEMINI API KEY
   - Set GEMINI_API_KEY environment variable
   - Get key from Google AI Studio

9. FIREBASE
   - Upload service account JSON file
   - Set FIREBASE_CREDENTIALS path

10. STATIC FILES
    - Run collectstatic before deployment
    - Use WhiteNoise for serving static files

11. LOGGING
    - Configure logging to file or service
    - Monitor error logs regularly

12. BACKUPS
    - Set up automated database backups
    - Test restore procedures

13. MONITORING
    - Set up error tracking (Sentry)
    - Set up performance monitoring
    - Set up uptime monitoring

14. EMAIL
    - Configure transactional email service
    - Set up SMTP credentials

DEPLOYMENT CHECKLIST
□ Use PostgreSQL with DATABASE_URL
□ Set unique SECRET_KEY
□ DEBUG=False
□ Configure ALLOWED_HOSTS
□ Update CORS_ALLOWED_ORIGINS
□ Set GEMINI_API_KEY
□ Upload Firebase credentials
□ Run migrations after deployment
□ Collect static files
□ Set up SSL certificate
□ Configure backup routines
□ Set up monitoring/logging
□ Test all endpoints in production
□ Verify JWT token flow
□ Check CORS headers
□ Test image uploads (if added)
□ Verify email notifications work
□ Check database performance
"""
