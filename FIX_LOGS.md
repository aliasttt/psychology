# رفع مشکل Logging

## مشکل:
```
FileNotFoundError: [Errno 2] No such file or directory: '/root/psychology/logs/django_errors.log'
```

## راه حل سریع (در سرور):

```bash
# ساخت پوشه logs
cd /root/psychology
mkdir -p logs
chmod 755 logs

# حالا دوباره migrate را اجرا کنید
python manage.py migrate
```

## یا اگر می‌خواهید از تنظیمات خودکار استفاده کنید:

فایل `settings.py` را به‌روزرسانی کردم تا به صورت خودکار پوشه `logs` را بسازد.

بعد از آپدیت فایل، دوباره امتحان کنید:

```bash
python manage.py migrate
```

## مسیر پروژه شما:

پروژه شما در `/root/psychology` است، نه `/srv/psychology_app/app`

پس دستورات را اینطور اجرا کنید:

```bash
cd /root/psychology
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```
