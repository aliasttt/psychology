# مراحل بعد از ساخت Superuser

## ✅ مرحله 1: جمع‌آوری Static Files

```bash
cd /root/psychology
python manage.py collectstatic --noinput
```

این دستور تمام فایل‌های CSS، JavaScript و تصاویر را در پوشه `staticfiles` جمع می‌کند.

---

## ✅ مرحله 2: تست کردن سرور (Development)

قبل از راه‌اندازی production، بهتر است سرور را تست کنید:

```bash
# بررسی تنظیمات
python manage.py check --deploy

# اجرای سرور توسعه
python manage.py runserver 0.0.0.0:8000
```

سپس در مرورگر:
- `http://your-server-ip:8000` - صفحه اصلی
- `http://your-server-ip:8000/admin` - پنل ادمین

**نکته:** بعد از تست، `Ctrl + C` بزنید تا سرور متوقف شود.

---

## ✅ مرحله 3: ساخت پوشه‌های مورد نیاز

```bash
# ساخت پوشه‌های static و media برای production
sudo mkdir -p /var/www/static
sudo mkdir -p /var/www/media
sudo chown -R www-data:www-data /var/www/static
sudo chown -R www-data:www-data /var/www/media
sudo chmod -R 755 /var/www/static
sudo chmod -R 755 /var/www/media
```

---

## ✅ مرحله 4: راه‌اندازی Gunicorn

### 4.1. ساخت پوشه‌های log و socket

```bash
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
sudo chown -R www-data:www-data /var/run/gunicorn
```

### 4.2. کپی کردن فایل systemd service

```bash
sudo cp /root/psychology/deployment/gunicorn.service /etc/systemd/system/psychology_clinic.service
```

### 4.3. ویرایش فایل service (اگر مسیرها متفاوت است)

```bash
sudo nano /etc/systemd/system/psychology_clinic.service
```

مطمئن شوید مسیرها درست باشند:
- `WorkingDirectory=/root/psychology`
- `ExecStart=/root/venv/bin/gunicorn` (یا مسیر virtual environment شما)

### 4.4. فعال و راه‌اندازی service

```bash
sudo systemctl daemon-reload
sudo systemctl enable psychology_clinic.service
sudo systemctl start psychology_clinic.service
sudo systemctl status psychology_clinic.service
```

### 4.5. بررسی لاگ‌ها (اگر خطا داشتید)

```bash
sudo journalctl -u psychology_clinic.service -f
```

---

## ✅ مرحله 5: تنظیم Nginx

### 5.1. کپی کردن فایل config

```bash
sudo cp /root/psychology/deployment/nginx.conf /etc/nginx/sites-available/psychology_clinic
```

### 5.2. ویرایش فایل config

```bash
sudo nano /etc/nginx/sites-available/psychology_clinic
```

**مهم:** 
- `server_name` را با domain یا IP سرور خود تغییر دهید
- مسیرهای static و media را بررسی کنید

### 5.3. Enable کردن site

```bash
# حذف default site (اختیاری)
sudo rm /etc/nginx/sites-enabled/default

# Enable کردن site جدید
sudo ln -s /etc/nginx/sites-available/psychology_clinic /etc/nginx/sites-enabled/

# تست configuration
sudo nginx -t
```

### 5.4. Reload Nginx

```bash
sudo systemctl reload nginx
sudo systemctl status nginx
```

---

## ✅ مرحله 6: تنظیم Firewall (UFW)

```bash
# بررسی وضعیت
sudo ufw status

# Allow HTTP و HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# اگر SSH روی پورت 22 است
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable
```

---

## ✅ مرحله 7: تنظیم SSL (HTTPS) - اختیاری

اگر domain دارید:

```bash
# نصب certbot
sudo apt install certbot python3-certbot-nginx

# دریافت SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# تست auto-renewal
sudo certbot renew --dry-run
```

---

## ✅ مرحله 8: تست نهایی

1. **بررسی Gunicorn:**
   ```bash
   sudo systemctl status psychology_clinic
   ```

2. **بررسی Nginx:**
   ```bash
   sudo systemctl status nginx
   ```

3. **بررسی Socket:**
   ```bash
   ls -la /var/run/gunicorn/psychology_clinic.sock
   ```

4. **تست در مرورگر:**
   - `http://your-server-ip` یا `http://your-domain.com`
   - `http://your-server-ip/admin` یا `http://your-domain.com/admin`

---

## 📝 خلاصه دستورات (کپی و پیست):

```bash
# 1. Collect static files
cd /root/psychology
python manage.py collectstatic --noinput

# 2. ساخت پوشه‌ها
sudo mkdir -p /var/www/{static,media}
sudo mkdir -p /var/log/gunicorn /var/run/gunicorn
sudo chown -R www-data:www-data /var/www/{static,media} /var/log/gunicorn /var/run/gunicorn

# 3. Gunicorn
sudo cp /root/psychology/deployment/gunicorn.service /etc/systemd/system/
sudo nano /etc/systemd/system/psychology_clinic.service  # ویرایش مسیرها
sudo systemctl daemon-reload
sudo systemctl enable psychology_clinic.service
sudo systemctl start psychology_clinic.service

# 4. Nginx
sudo cp /root/psychology/deployment/nginx.conf /etc/nginx/sites-available/psychology_clinic
sudo nano /etc/nginx/sites-available/psychology_clinic  # ویرایش domain
sudo ln -s /etc/nginx/sites-available/psychology_clinic /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 5. Firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 🎯 بعد از راه‌اندازی:

1. **ورود به Admin Panel:**
   - آدرس: `http://your-domain.com/admin`
   - با username و password که ساختید وارد شوید

2. **ایجاد محتوا:**
   - Blog categories و posts
   - Services
   - FAQs

3. **بررسی لاگ‌ها:**
   ```bash
   sudo tail -f /var/log/gunicorn/error.log
   sudo tail -f /var/log/nginx/error.log
   ```

---

**موفق باشید! 🎉**
