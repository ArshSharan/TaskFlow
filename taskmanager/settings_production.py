"""
Production settings for Render deployment
"""

from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your Render domain here
ALLOWED_HOSTS = [
    '*.onrender.com',  # This will work with any Render subdomain
    'taskflow-django.onrender.com',  # Replace with your actual Render domain
    'localhost',
    '127.0.0.1',
]

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Static files settings for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Database configuration for TiDB with SSL certificate handling
import tempfile
import base64

def create_ssl_cert_from_env():
    """Create SSL certificate file from environment variable for TiDB connection"""
    cert_content = os.environ.get('TIDB_SSL_CERT_B64')
    if cert_content:
        # Decode base64 content
        cert_decoded = base64.b64decode(cert_content).decode('utf-8')
        
        # Create temporary certificate file
        cert_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.pem', delete=False)
        cert_file.write(cert_decoded)
        cert_file.close()
        
        return cert_file.name
    return None

# Create SSL certificate file for TiDB if in production
if 'TIDB_SSL_CERT_B64' in os.environ:
    ssl_cert_path = create_ssl_cert_from_env()
    if ssl_cert_path:
        # Update database configuration to use the certificate
        DATABASES['default']['OPTIONS'] = {
            'ssl': {
                'ca': ssl_cert_path
            }
        }

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://*.onrender.com",  # This will work with any Render subdomain
    "https://taskflow-django.onrender.com",  # Replace with your actual domain
]

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
