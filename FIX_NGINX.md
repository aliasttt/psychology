# رفع مشکل Nginx

## مشکل:
```
cp: cannot create regular file '/etc/nginx/sites-available/psychology_clinic': No such file or directory
```

## علت:
یا Nginx نصب نشده یا پوشه `sites-available` وجود ندارد.

## راه حل:

### 1. بررسی نصب Nginx:

```bash
sudo systemctl status nginx
```

اگر نصب نشده:
```bash
sudo apt update
sudo apt install nginx -y
```

### 2. بررسی وجود پوشه:

```bash
ls -la /etc/nginx/
```

اگر پوشه `sites-available` وجود ندارد:
```bash
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled
```

### 3. ساخت فایل config به صورت مستقیم:

```bash
sudo nano /etc/nginx/sites-available/psychology_clinic
```

محتوای فایل را از `deployment/nginx.conf` کپی کنید.

### 4. یا استفاده از مسیر دیگری:

اگر ساختار Nginx متفاوت است، می‌توانید فایل را در مسیر اصلی قرار دهید:

```bash
sudo cp /root/psychology/deployment/nginx.conf /etc/nginx/conf.d/psychology_clinic.conf
```

یا:

```bash
sudo nano /etc/nginx/nginx.conf
```

و محتوا را در بخش `http` اضافه کنید.
