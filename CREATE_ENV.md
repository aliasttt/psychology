# ساخت فایل .env

## مشکل:
```
psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: fe_sendauth: no password supplied
```

## علت:
فایل `.env` وجود ندارد یا رمز عبور دیتابیس در آن تنظیم نشده است.

## راه حل:

### 1. ساخت فایل .env

```bash
cd /root/psychology
nano .env
```

### 2. محتوای فایل .env (کپی و پیست کنید):

```env
DEBUG=False
SECRET_KEY=django-insecure-change-this-to-secure-key-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,your-server-ip

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

### 3. تولید SECRET_KEY جدید (اختیاری اما توصیه می‌شود):

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

خروجی را کپی کنید و در فایل `.env` به جای `django-insecure-change-this-to-secure-key-in-production` بگذارید.

### 4. امن کردن فایل .env:

```bash
chmod 600 .env
```

### 5. بررسی فایل:

```bash
cat .env
```

### 6. حالا دوباره migrate را اجرا کنید:

```bash
python manage.py migrate
```

## نکات مهم:

1. **رمز عبور دیتابیس**: `Aasadi2323#` (همان رمزی که در PostgreSQL ساختید)
2. **ALLOWED_HOSTS**: IP سرور خود را اضافه کنید
3. **SECRET_KEY**: برای production حتماً یک کلید جدید تولید کنید
4. **فایل .env**: نباید در git commit شود (در .gitignore است)

## اگر هنوز خطا گرفتید:

بررسی کنید:
- فایل `.env` در مسیر `/root/psychology/.env` باشد
- رمز عبور درست باشد: `Aasadi2323#`
- نام دیتابیس درست باشد: `psychology_db`
- نام کاربر درست باشد: `psychology_user`
