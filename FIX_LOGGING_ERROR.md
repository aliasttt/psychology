# رفع خطای Logging

## مشکل:
```
ValueError: Unable to configure handler 'file'
```

Gunicorn نمی‌تواند فایل لاگ را بسازد یا به آن دسترسی ندارد.

## راه حل:

### 1. ساخت پوشه logs و اعطای دسترسی:

```bash
cd /root/psychology
mkdir -p logs
sudo chown -R www-data:www-data logs
sudo chmod -R 755 logs
```

### 2. Restart Gunicorn:

```bash
sudo systemctl restart psychology_clinic.service
sudo systemctl status psychology_clinic.service
```

### 3. بررسی لاگ:

```bash
sudo tail -20 /var/log/gunicorn/error.log
```
