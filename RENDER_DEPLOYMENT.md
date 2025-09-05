# TaskFlow - Render Deployment Guide

## 🚀 Quick Deployment Checklist

### 1. Database Migration Options

#### Option A: Start Fresh (Recommended for new deployments)
- ✅ Clean slate
- ✅ No data migration needed
- ❌ You'll lose existing tasks

#### Option B: Export & Import Data
- ✅ Keep all existing data
- ❌ More complex setup
- ❌ Need to handle data formatting

### 2. What to Push to GitHub

#### ✅ Include These Files:
```
taskmanager/
├── __init__.py
├── settings.py
├── settings_render.py  # NEW - Production settings
├── urls.py
├── wsgi.py
├── asgi.py

tasks/
├── All your app files
├── migrations/
├── static/
├── templates/

requirements.txt        # UPDATED - Added production packages
build.sh               # NEW - Render build script
manage.py
README.md
```

#### ❌ DON'T Push These:
```
__pycache__/           # Python cache files
*.pyc                  # Compiled Python files
.env                   # Environment variables (contains secrets)
db.sqlite3             # Local database
media/                 # User uploaded files (use cloud storage)
venv/                  # Virtual environment
.DS_Store              # Mac system files
Thumbs.db              # Windows system files
*.log                  # Log files
```

### 3. Pre-Push Setup

#### Create .gitignore file:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```

## 🗄️ Database Migration Guide

### Option A: Fresh Start (Recommended)

1. **No action needed** - Render will create empty database
2. **After deployment**, create superuser:
   ```bash
   # In Render shell
   python manage.py createsuperuser --settings=taskmanager.settings_render
   ```

### Option B: Migrate Existing Data

#### Step 1: Export your local data
```bash
# In your local project directory
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datadump.json
```

#### Step 2: After Render deployment
```bash
# In Render shell
python manage.py loaddata datadump.json --settings=taskmanager.settings_render
```

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

1. **Create .gitignore** (see above)
2. **Add new files** to your project:
   - `settings_render.py`
   - `build.sh`
   - Updated `requirements.txt`

### Step 2: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add gitignore
git add .gitignore

# Add all files
git add .

# Commit
git commit -m "Prepare TaskFlow for Render deployment"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/taskflow-app.git

# Push
git push -u origin main
```

### Step 3: Deploy on Render

1. **Go to [render.com](https://render.com)** and sign up
2. **Connect GitHub** account
3. **Create Web Service**:
   - Choose your repository
   - Name: `taskflow-app`
   - Environment: `Python 3`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn taskmanager.wsgi:application --settings=taskmanager.settings_render`

4. **Create PostgreSQL Database**:
   - Click "New" → "PostgreSQL"
   - Name: `taskflow-database`
   - Choose free plan

5. **Connect Database to Web Service**:
   - In your web service settings
   - Add environment variable: `DATABASE_URL` = (copy from your database)

### Step 4: Environment Variables in Render

Add these in your Web Service environment variables:
```
DJANGO_SETTINGS_MODULE=taskmanager.settings_render
SECRET_KEY=your-secret-key-here-make-it-long-and-random
DEBUG=False
```

### Step 5: Post-Deployment

1. **Create superuser** in Render shell
2. **Test your application**
3. **Add custom domain** (optional)

## 🔧 Troubleshooting

### Common Issues:

1. **Build fails**: Check `build.sh` permissions
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build script executable"
   git push
   ```

2. **Database connection fails**: Verify `DATABASE_URL` is set correctly

3. **Static files not loading**: Check `STATIC_ROOT` in settings

4. **CORS errors**: Add your Render domain to `CORS_ALLOWED_ORIGINS`

## 💰 Render Pricing

- **Web Service**: Free (with limitations)
- **PostgreSQL**: Free (1GB storage)
- **Custom Domain**: Free
- **SSL Certificate**: Free

**Free tier limitations**:
- Service sleeps after 15 minutes of inactivity
- 750 hours/month runtime limit
- 1GB RAM, 0.5 CPU

## 🎯 Next Steps After Deployment

1. **Test all functionality**
2. **Set up monitoring** (Render provides basic metrics)
3. **Configure backups** (database snapshots)
4. **Add custom domain** when ready
5. **Upgrade to paid plan** when you outgrow free tier

## 📞 Need Help?

If you encounter issues:
1. Check Render logs in dashboard
2. Review Django error pages
3. Verify environment variables
4. Test database connection

Your TaskFlow app will be live at: `https://your-app-name.onrender.com`
