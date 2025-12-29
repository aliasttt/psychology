# رفع مشکل نهایی - بررسی اتصال

## مراحل بررسی:

### 1. تست مستقیم Gunicorn:

```bash
curl --unix-socket /var/run/gunicorn/psychology_clinic.sock http://localhost/
```

اگر این کار کرد، Gunicorn درست است و مشکل از Nginx است.

### 2. بررسی فایل Nginx config:

```bash
cat /etc/nginx/sites-available/psychology_clinic
```

مطمئن شوید:
- `upstream` به `/var/run/gunicorn/psychology_clinic.sock` اشاره می‌کند
- `server_name` درست است
- `proxy_pass` به `http://psychology_clinic` اشاره می‌کند

### 3. Restart کامل همه سرویس‌ها:

```bash
sudo systemctl restart psychology_clinic.service
sudo systemctl restart nginx
```

### 4. بررسی لاگ‌ها به صورت real-time:

```bash
# Terminal 1
sudo tail -f /var/log/nginx/error.log

# Terminal 2 (در مرورگر refresh کنید)
# یا
sudo tail -f /var/log/gunicorn/error.log
```

### 5. بررسی access log:

```bash
sudo tail -f /var/log/nginx/access.log
```

سپس در مرورگر refresh کنید و ببینید آیا درخواست ثبت می‌شود.
