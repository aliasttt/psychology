# Production Deployment Guide - Psychology Clinic Django Application

This guide provides step-by-step instructions for deploying the Psychology Clinic Django application to an Ubuntu 22.04 VPS.

## Prerequisites

- Ubuntu 22.04 VPS with root/sudo access
- Domain name pointing to your VPS IP (e.g., psychotherapy-clinic.com)
- SSH access to your server

---

## Step 1: Create Non-Root User & Secure SSH

```bash
# Create a new user
sudo adduser psychology_user
sudo usermod -aG sudo psychology_user

# Switch to the new user
su - psychology_user

# Secure SSH (edit as root)
sudo nano /etc/ssh/sshd_config

# Set these values:
# PermitRootLogin no
# PasswordAuthentication no  # After setting up SSH keys
# Port 2222  # Optional: change default port

# Restart SSH
sudo systemctl restart sshd
```

---

## Step 2: Update System & Install Packages

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    nginx \
    ufw \
    git \
    build-essential \
    libpq-dev \
    python3-dev
```

---

## Step 3: Setup PostgreSQL Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Inside PostgreSQL prompt, run:
CREATE DATABASE psychology_db;
CREATE USER psychology_user WITH PASSWORD 'YOUR_SECURE_DB_PASSWORD_HERE';
ALTER ROLE psychology_user SET client_encoding TO 'utf8';
ALTER ROLE psychology_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE psychology_user SET timezone TO 'Europe/Istanbul';
GRANT ALL PRIVILEGES ON DATABASE psychology_db TO psychology_user;
\q

# Verify connection
sudo -u postgres psql -c "\l" | grep psychology_db
```

**Important:** Replace `YOUR_SECURE_DB_PASSWORD_HERE` with a strong password. Save it securely.

---

## Step 4: Create Application Directory Structure

```bash
# Create directories
sudo mkdir -p /srv/psychology_app/{app,env}
sudo mkdir -p /var/www/{static,media}
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn

# Set ownership
sudo chown -R psychology_user:www-data /srv/psychology_app
sudo chown -R www-data:www-data /var/www/{static,media}
sudo chown -R www-data:www-data /var/log/gunicorn
sudo chown -R www-data:www-data /var/run/gunicorn

# Set permissions
sudo chmod -R 755 /srv/psychology_app
sudo chmod -R 755 /var/www/{static,media}
sudo chmod 755 /var/log/gunicorn
sudo chmod 755 /var/run/gunicorn
```

---

## Step 5: Clone/Upload Application Code

```bash
# Navigate to app directory
cd /srv/psychology_app/app

# Option 1: If using Git
git clone YOUR_REPOSITORY_URL .

# Option 2: If uploading via SCP/SFTP
# Upload all project files to /srv/psychology_app/app/
```

---

## Step 6: Setup Python Virtual Environment

```bash
cd /srv/psychology_app

# Create virtual environment
python3.12 -m venv env

# Activate virtual environment
source env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
cd app
pip install -r requirements.txt
```

---

## Step 7: Configure Environment Variables

```bash
# Create .env file
cd /srv/psychology_app/app
nano .env
```

Add the following content (replace with your actual values):

```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here-generate-with-openssl-rand-hex-32
ALLOWED_HOSTS=psychotherapy-clinic.com,www.psychotherapy-clinic.com,YOUR_SERVER_IP

DB_NAME=psychology_db
DB_USER=psychology_user
DB_PASSWORD=YOUR_SECURE_DB_PASSWORD_HERE
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

TIMEZONE=Europe/Istanbul

CSRF_TRUSTED_ORIGINS=https://psychotherapy-clinic.com,https://www.psychotherapy-clinic.com

STATIC_ROOT=/var/www/static
MEDIA_ROOT=/var/www/media
```

**Generate SECRET_KEY:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Secure the .env file:**
```bash
chmod 600 .env
```

---

## Step 8: Run Django Migrations & Create Superuser

```bash
cd /srv/psychology_app/app
source ../env/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Create logs directory
mkdir -p logs
chmod 755 logs
```

---

## Step 9: Test Django Application

```bash
# Test that everything works
python manage.py check --deploy

# Test runserver (optional, for testing)
python manage.py runserver 0.0.0.0:8000
# Visit http://YOUR_SERVER_IP:8000 to test
# Press Ctrl+C to stop
```

---

## Step 10: Configure Gunicorn

```bash
# Create systemd service file
sudo nano /etc/systemd/system/psychology_clinic.service
```

Paste the content from `deployment/gunicorn.service` file, then:

```bash
# Create required directories
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
sudo chown -R www-data:www-data /var/run/gunicorn

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable psychology_clinic.service

# Start the service
sudo systemctl start psychology_clinic.service

# Check status
sudo systemctl status psychology_clinic.service

# View logs if there are issues
sudo journalctl -u psychology_clinic.service -f
```

---

## Step 11: Configure Nginx

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/psychology_clinic
```

Paste the content from `deployment/nginx.conf` file.

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/psychology_clinic /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# If test passes, reload Nginx
sudo systemctl reload nginx

# Check Nginx status
sudo systemctl status nginx
```

---

## Step 12: Setup HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate (replace with your domain)
sudo certbot --nginx -d psychotherapy-clinic.com -d www.psychotherapy-clinic.com

# Follow the prompts:
# - Enter your email
# - Agree to terms
# - Choose whether to redirect HTTP to HTTPS (recommended: Yes)

# Test auto-renewal
sudo certbot renew --dry-run

# Certbot automatically sets up auto-renewal via cron
# Verify: sudo systemctl status certbot.timer
```

**After SSL is configured, update Nginx config:**
```bash
sudo nano /etc/nginx/sites-available/psychology_clinic
# Uncomment the HTTPS server block and comment out the HTTP redirect
sudo nginx -t
sudo systemctl reload nginx
```

---

## Step 13: Configure Firewall (UFW)

```bash
# Check UFW status
sudo ufw status

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow 22/tcp
# Or if you changed SSH port:
# sudo ufw allow 2222/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS
sudo ufw allow 443/tcp

# Enable UFW
sudo ufw enable

# Check status
sudo ufw status verbose
```

---

## Step 14: Final Configuration Checks

### Update Django Settings for Production

Ensure your `.env` file has:
- `DEBUG=False`
- `ALLOWED_HOSTS` includes your domain
- `CSRF_TRUSTED_ORIGINS` includes your HTTPS domain

### Verify Services

```bash
# Check all services are running
sudo systemctl status psychology_clinic
sudo systemctl status nginx
sudo systemctl status postgresql

# Check Gunicorn socket exists
ls -la /run/gunicorn/psychology_clinic.sock

# Check logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/nginx/error.log
```

---

## Step 15: Post-Deployment Tasks

### Create Initial Content

1. Access admin panel: `https://psychotherapy-clinic.com/admin`
2. Create:
   - Blog categories and posts
   - Services with descriptions
   - FAQs

### Setup Log Rotation

```bash
sudo nano /etc/logrotate.d/psychology-clinic
```

Add:
```
/var/log/gunicorn/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

---

## Troubleshooting

### Gunicorn Issues

```bash
# Check service status
sudo systemctl status psychology_clinic

# View logs
sudo journalctl -u psychology_clinic.service -n 50

# Restart service
sudo systemctl restart psychology_clinic
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Reload configuration
sudo systemctl reload nginx
```

### Database Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
sudo -u postgres psql -d psychology_db -c "SELECT 1;"
```

### Permission Issues

```bash
# Fix static/media permissions
sudo chown -R www-data:www-data /var/www/{static,media}
sudo chmod -R 755 /var/www/{static,media}

# Fix app directory permissions
sudo chown -R psychology_user:www-data /srv/psychology_app
```

---

## Maintenance Commands

### Update Application Code

```bash
cd /srv/psychology_app/app
source ../env/bin/activate
git pull  # or upload new files
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart psychology_clinic
```

### Backup Database

```bash
# Create backup
sudo -u postgres pg_dump psychology_db > backup_$(date +%Y%m%d).sql

# Restore backup
sudo -u postgres psql psychology_db < backup_YYYYMMDD.sql
```

### View Logs

```bash
# Gunicorn logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Django logs
tail -f /srv/psychology_app/app/logs/django_errors.log
```

---

## Security Checklist

- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY in .env
- [ ] .env file has 600 permissions
- [ ] ALLOWED_HOSTS configured correctly
- [ ] CSRF_TRUSTED_ORIGINS set for HTTPS
- [ ] SSL certificate installed and auto-renewal enabled
- [ ] Firewall (UFW) configured
- [ ] SSH secured (no root login, key-based auth)
- [ ] Database user has limited privileges
- [ ] Regular backups scheduled
- [ ] System packages updated regularly

---

## Performance Optimization

### Gunicorn Workers

Edit `/etc/systemd/system/psychology_clinic.service`:
- Adjust `--workers` based on CPU cores: `(2 x CPU cores) + 1`

### Nginx Caching

Add to Nginx config for better performance:
```nginx
# In server block
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=psychology_cache:10m max_size=100m;
proxy_cache_key "$scheme$request_method$host$request_uri";
```

---

## Support

For issues or questions:
1. Check logs first
2. Verify all services are running
3. Test configuration files
4. Review this deployment guide

---

**Deployment completed successfully!** 🎉

Your Django application should now be accessible at `https://psychotherapy-clinic.com`
