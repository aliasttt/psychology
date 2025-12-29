# رفع مشکل CHDIR (تغییر دایرکتوری)

## مشکل:
```
status=200/CHDIR
```

این یعنی Gunicorn نمی‌تواند به `WorkingDirectory` تغییر کند.

## علت:
مشکل دسترسی است - کاربر `www-data` به مسیر `/root/psychology` دسترسی ندارد.

## راه حل:

### 1. بررسی مسیر:

```bash
ls -la /root/psychology
```

### 2. اعطای دسترسی به www-data:

```bash
# اعطای دسترسی خواندن به پوشه psychology
sudo chmod 755 /root/psychology

# اعطای دسترسی به فایل‌های پروژه
sudo chown -R root:www-data /root/psychology
sudo chmod -R 755 /root/psychology

# اعطای دسترسی به فایل .env
sudo chmod 644 /root/psychology/.env
```

### 3. یا بهتر است: تغییر WorkingDirectory به مسیر قابل دسترسی

اگر نمی‌خواهید دسترسی root را تغییر دهید، می‌توانید از یک مسیر دیگر استفاده کنید:

```bash
# ساخت مسیر جدید
sudo mkdir -p /srv/psychology_app
sudo cp -r /root/psychology/* /srv/psychology_app/
sudo chown -R www-data:www-data /srv/psychology_app
sudo chmod -R 755 /srv/psychology_app
```

سپس فایل service را ویرایش کنید:
```ini
WorkingDirectory=/srv/psychology_app
```

### 4. راه حل سریع (توصیه می‌شود):

```bash
# اعطای دسترسی
sudo chmod 755 /root
sudo chmod 755 /root/psychology
sudo chown -R root:www-data /root/psychology
sudo chmod -R 755 /root/psychology

# Restart service
sudo systemctl restart psychology_clinic.service
sudo systemctl status psychology_clinic.service
```

### 5. بررسی لاگ‌ها:

```bash
sudo journalctl -u psychology_clinic.service -n 50 --no-pager
```
