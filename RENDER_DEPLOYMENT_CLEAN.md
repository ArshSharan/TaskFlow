# TaskFlow - Render Deployment Guide

## Prerequisites
✅ TiDB Cloud database configured
✅ Repository cleaned and ready for GitHub
✅ Production settings configured

## Step 1: Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment with TiDB"
git push origin main
```

## Step 2: Render Setup

1. **Go to [Render.com](https://render.com)**
2. **Connect your GitHub account**
3. **Create New Web Service**
4. **Connect your repository**

## Step 3: Configure Web Service

### Basic Settings:
- **Name**: `taskflow-django` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your location
- **Branch**: `main`

### Build & Deploy Settings:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn taskmanager.wsgi:application --bind 0.0.0.0:$PORT --settings=taskmanager.settings_production`

### Environment Variables:
Add these in Render's Environment section:

```
DJANGO_SECRET_KEY=your-secret-key-here
DB_NAME=your-tidb-database-name
DB_USER=your-tidb-username
DB_PASSWORD=your-tidb-password
DB_HOST=gateway01.ap-southeast-1.prod.aws.tidbcloud.com
DB_PORT=4000
DB_SSL_CA=./certs/ca-cert.pem
DJANGO_SETTINGS_MODULE=taskmanager.settings_production
```

## Step 4: SSL Certificate
The TiDB SSL certificate (`isrgrootx1.pem`) is already included in your repository in the `certs/` folder.

## Step 5: Deploy
1. **Click "Create Web Service"**
2. **Wait for deployment** (5-10 minutes)
3. **Your app will be available** at: `https://your-app-name.onrender.com`

## Step 6: Post-Deployment
1. **Create superuser** (if needed):
   ```bash
   python manage.py createsuperuser --settings=taskmanager.settings_production
   ```
   
2. **Update ALLOWED_HOSTS** in `settings_production.py` with your actual Render domain

## Important Notes:
- ✅ TiDB connection configured for production
- ✅ Static files handling with WhiteNoise
- ✅ Security settings enabled
- ✅ SSL/HTTPS enforced
- ✅ Media files configured

## Troubleshooting:
- Check Render logs if deployment fails
- Ensure all environment variables are set correctly
- Verify TiDB connection details

Your TaskFlow app will be live and accessible worldwide! 🚀
