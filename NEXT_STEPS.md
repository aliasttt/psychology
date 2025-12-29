# مراحل بعدی - راه‌اندازی Django

## ✅ مرحله 1: دیتابیس آماده است!

دیتابیس `psychology_db` و کاربر `psychology_user` با موفقیت ایجاد شدند.

---

## 📝 مرحله 2: تنظیم فایل .env

فایل `.env` را ایجاد و تنظیم کنید:

```bash
cd /srv/psychology_app/app  # یا مسیر پروژه شما
nano .env
```

محتوای فایل `.env` (با اطلاعات دیتابیس شما):

```env
DEBUG=False
SECRET_KEY=your-secret-key-here-generate-new-one
ALLOWED_HOSTS=your-server-ip,your-domain.com,localhost,127.0.0.1

DB_NAME=psychology_db
DB_USER=psychology_user
DB_PASSWORD=Aasadi2323#
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

TIMEZONE=Europe/Istanbul

CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com

STATIC_ROOT=/var/www/static
MEDIA_ROOT=/var/www/media
```

**تولید SECRET_KEY جدید:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**امن کردن فایل .env:**
```bash
chmod 600 .env
```

---

## 🐍 مرحله 3: نصب Dependencies و راه‌اندازی Virtual Environment

```bash
# اگر virtual environment ندارید، بسازید
cd /srv/psychology_app
python3 -m venv env

# فعال کردن virtual environment
source env/bin/activate

# نصب dependencies
cd app
pip install -r requirements.txt
```

---

## 🗄️ مرحله 4: اجرای Migrations

```bash
# مطمئن شوید virtual environment فعال است
source /srv/psychology_app/env/bin/activate

# اجرای migrations
cd /srv/psychology_app/app
python manage.py migrate
```

اگر خطا گرفتید، بررسی کنید:
- فایل `.env` درست تنظیم شده باشد
- PostgreSQL در حال اجرا باشد: `sudo systemctl status postgresql`

---

## 👤 مرحله 5: ایجاد Superuser

```bash
python manage.py createsuperuser
```

اطلاعات را وارد کنید:
- Username
- Email (اختیاری)
- Password (دو بار)

---

## 📦 مرحله 6: جمع‌آوری Static Files

```bash
python manage.py collectstatic --noinput
```

---

## ✅ مرحله 7: تست Django

```bash
# بررسی تنظیمات
python manage.py check --deploy

# اجرای سرور توسعه (برای تست)
python manage.py runserver 0.0.0.0:8000
```

سپس در مرورگر: `http://your-server-ip:8000`

---

## 🔧 مرحله 8: راه‌اندازی Gunicorn (Production)

بعد از اینکه مطمئن شدید همه چیز کار می‌کند:

```bash
# کپی کردن فایل systemd service
sudo cp /srv/psychology_app/app/deployment/gunicorn.service /etc/systemd/system/psychology_clinic.service

# ویرایش مسیرها در فایل (اگر نیاز باشد)
sudo nano /etc/systemd/system/psychology_clinic.service

# Reload systemd
sudo systemctl daemon-reload

# Enable و Start service
sudo systemctl enable psychology_clinic.service
sudo systemctl start psychology_clinic.service

# بررسی وضعیت
sudo systemctl status psychology_clinic.service
```

---

## 🌐 مرحله 9: تنظیم Nginx

```bash
# کپی کردن فایل nginx config
sudo cp /srv/psychology_app/app/deployment/nginx.conf /etc/nginx/sites-available/psychology_clinic

# ویرایش domain name در فایل
sudo nano /etc/nginx/sites-available/psychology_clinic

# Enable site
sudo ln -s /etc/nginx/sites-available/psychology_clinic /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

---

## 🔒 مرحله 10: تنظیم SSL (HTTPS)

```bash
# نصب certbot
sudo apt install certbot python3-certbot-nginx

# دریافت SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# تست auto-renewal
sudo certbot renew --dry-run
```

---

## 📋 خلاصه دستورات (کپی و پیست)

```bash
# 1. ساخت virtual environment (اگر ندارید)
cd /srv/psychology_app
python3 -m venv env
source env/bin/activate

# 2. نصب dependencies
cd app
pip install -r requirements.txt

# 3. ساخت .env (با nano یا vim)
nano .env
# محتوای .env را از بالا کپی کنید

# 4. امن کردن .env
chmod 600 .env

# 5. Migrations
python manage.py migrate

# 6. Superuser
python manage.py createsuperuser

# 7. Static files
python manage.py collectstatic --noinput

# 8. تست
python manage.py check --deploy
python manage.py runserver 0.0.0.0:8000
```

---

## ❓ مشکلات رایج

### خطای اتصال به دیتابیس:
```bash
# بررسی PostgreSQL
sudo systemctl status postgresql
sudo systemctl start postgresql

# تست اتصال
psql -U psychology_user -d psychology_db -h localhost
```

### خطای Module not found:
```bash
# مطمئن شوید virtual environment فعال است
source /srv/psychology_app/env/bin/activate
pip install -r requirements.txt
```

### خطای Permission denied:
```bash
# بررسی دسترسی‌ها
ls -la /srv/psychology_app/app/.env
chmod 600 /srv/psychology_app/app/.env
```

---

**موفق باشید! 🎉**
