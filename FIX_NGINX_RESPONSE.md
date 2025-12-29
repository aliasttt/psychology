# رفع مشکل عدم پاسخ Nginx

## مشکل:
- Nginx در حال اجرا است
- Gunicorn در حال اجرا است
- Firewall باز است
- اما سایت قابل دسترسی نیست

## راه حل:

### 1. بررسی فایل config Nginx:

```bash
cat /etc/nginx/sites-available/psychology_clinic
```

مطمئن شوید:
- `server_name` درست است
- `upstream` به socket درست اشاره می‌کند
- مسیرهای static و media درست هستند

### 2. تست Nginx config:

```bash
sudo nginx -t
```

### 3. Restart کامل Nginx (نه reload):

```bash
sudo systemctl restart nginx
sudo systemctl status nginx
```

### 4. بررسی access log:

```bash
sudo tail -20 /var/log/nginx/access.log
```

### 5. تست مستقیم Gunicorn:

```bash
curl --unix-socket /var/run/gunicorn/psychology_clinic.sock http://localhost/
```

اگر این کار کرد، مشکل از Nginx config است.

### 6. بررسی ALLOWED_HOSTS:

```bash
cat /root/psychology/.env | grep ALLOWED_HOSTS
```

باید IP سرور را شامل شود: `141.98.51.168`
