# رفع مشکل SSL Redirect

## مشکل:
```
HTTP/1.1 301 Moved Permanently
Location: https://141.98.51.168/
```

Django به HTTPS redirect می‌کند اما SSL هنوز تنظیم نشده.

## راه حل:

فایل `settings.py` را آپدیت کردم تا SSL redirect غیرفعال شود تا زمانی که SSL تنظیم شود.

### بعد از آپدیت:

```bash
# Restart Gunicorn
sudo systemctl restart psychology_clinic.service

# بررسی وضعیت
sudo systemctl status psychology_clinic.service
```

### بعد از تنظیم SSL:

وقتی SSL را تنظیم کردید، در `settings.py` این خطوط را uncomment کنید:
- `SECURE_SSL_REDIRECT = True`
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`

و خطوط `False` را comment کنید.
