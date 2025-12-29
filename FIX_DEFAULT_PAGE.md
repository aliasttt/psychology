# رفع مشکل نمایش صفحه پیش‌فرض Nginx

## مشکل:
صفحه "Welcome to nginx!" نمایش داده می‌شود به جای سایت Django.

## علت:
احتمالاً default site هنوز فعال است یا site جدید enable نشده.

## راه حل:

### 1. بررسی sites-enabled:

```bash
ls -la /etc/nginx/sites-enabled/
```

باید فقط `psychology_clinic` باشد، نه `default`.

### 2. حذف default site:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

### 3. بررسی enable شدن site جدید:

```bash
ls -la /etc/nginx/sites-enabled/
```

باید `psychology_clinic` را ببینید.

اگر نیست:
```bash
sudo ln -s /etc/nginx/sites-available/psychology_clinic /etc/nginx/sites-enabled/
```

### 4. بررسی Gunicorn:

```bash
sudo systemctl status psychology_clinic.service
```

باید `active (running)` باشد.

### 5. بررسی Socket:

```bash
ls -la /var/run/gunicorn/psychology_clinic.sock
```

باید وجود داشته باشد.

### 6. Reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 7. بررسی لاگ‌ها:

```bash
# لاگ Nginx
sudo tail -20 /var/log/nginx/error.log

# لاگ Gunicorn
sudo tail -20 /var/log/gunicorn/error.log
```
