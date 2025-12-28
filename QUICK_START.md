# Quick Start Guide

## Local Development Setup

### 1. Prerequisites
- Python 3.12 or higher
- PostgreSQL (or SQLite for quick testing)
- pip

### 2. Setup Steps

```bash
# Clone or navigate to project directory
cd psichlogy

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example .env

# Edit .env file with your settings
# For development, you can use SQLite by commenting out PostgreSQL settings
```

### 3. Database Setup (PostgreSQL)

```bash
# Create database
createdb psychology_db

# Or use psql
psql -U postgres
CREATE DATABASE psychology_db;
\q
```

### 4. Run Migrations

```bash
# Activate virtual environment first
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit:
- http://127.0.0.1:8000 - Main site
- http://127.0.0.1:8000/admin - Admin panel

### 6. Create Initial Content

1. Login to admin panel
2. Create blog categories and posts
3. Create services with descriptions
4. Add FAQs to services

## Common Issues

### Issue: Module not found
**Solution:** Make sure virtual environment is activated and dependencies are installed.

### Issue: Database connection error
**Solution:** Check PostgreSQL is running and database credentials in .env are correct.

### Issue: Static files not loading
**Solution:** Run `python manage.py collectstatic` and check STATIC_ROOT in settings.

### Issue: Permission denied
**Solution:** Check file permissions, especially for media and static directories.

## Next Steps

- See [README.md](README.md) for full documentation
- See [deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md) for production deployment
