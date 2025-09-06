"""
Production settings for Render deployment
"""

from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
# Enable DEBUG temporarily for troubleshooting 400 errors
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Enable template debugging
if DEBUG:
    TEMPLATES[0]['OPTIONS']['debug'] = True

# Add your Render domain here
# Get the allowed hosts from environment variable for flexibility
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# Add Render hostname if available
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Also add common Render patterns
ALLOWED_HOSTS.extend([
    'taskflow-django.onrender.com',
    'django-mariadb-app.onrender.com',
    'taskflow.onrender.com',
])

# Security settings for production (relaxed for initial deployment)
# Note: Enable these gradually once basic functionality works
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SECURE_HSTS_SECONDS = 31536000 if SECURE_SSL_REDIRECT else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_SSL_REDIRECT
SECURE_HSTS_PRELOAD = SECURE_SSL_REDIRECT
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

# CORS settings for production (initially permissive for debugging)
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'
CORS_ALLOWED_ORIGINS = []

# If not allowing all origins, specify allowed origins
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = [
        "https://taskflow-django.onrender.com",
        "https://django-mariadb-app.onrender.com", 
        "https://taskflow.onrender.com",
    ]
    # Add the render hostname if available
    if RENDER_EXTERNAL_HOSTNAME:
        CORS_ALLOWED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

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
