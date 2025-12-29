# رفع مشکل اتصال به دیتابیس

## مشکل:
```
django.db.utils.ProgrammingError: invalid dsn: invalid connection option "charset"
```

## علت:
PostgreSQL از `charset` در OPTIONS پشتیبانی نمی‌کند. PostgreSQL به صورت پیش‌فرض UTF-8 است و نیازی به تنظیم charset نیست.

## راه حل:

فایل `settings.py` را اصلاح کردم و `charset` را حذف کردم.

همچنین مشکل URL تکراری `blog/` را هم رفع کردم.

## بعد از آپدیت فایل:

```bash
cd /root/psychology
git pull  # اگر از git استفاده می‌کنید
# یا فایل settings.py را دستی آپدیت کنید

# حالا دوباره migrate را اجرا کنید
python manage.py migrate
```

## اگر فایل را دستی آپدیت می‌کنید:

در فایل `psychology_clinic/settings.py`، بخش DATABASES را اینطور تغییر دهید:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='psychology_db'),
        'USER': env('DB_USER', default='psychology_user'),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
        # OPTIONS را کاملاً حذف کنید یا خالی بگذارید
    }
}
```

## همچنین:

در فایل `psychology_clinic/urls.py`، خط تکراری `path('blog/', include('blog.urls'))` را حذف کنید.
