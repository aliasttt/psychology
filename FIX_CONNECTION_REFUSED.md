# رفع مشکل ERR_CONNECTION_REFUSED

## مشکل:
```
ERR_CONNECTION_REFUSED
141.98.51.168 refused to connect
```

## علت:
احتمالاً Firewall پورت 80 را بسته یا Nginx در حال اجرا نیست.

## راه حل:

### 1. بررسی وضعیت Nginx:

```bash
sudo systemctl status nginx
```

اگر در حال اجرا نیست:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 2. بررسی Firewall:

```bash
sudo ufw status
```

اگر فعال است و پورت 80 اجازه ندارد:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

### 3. بررسی پورت‌های باز:

```bash
sudo netstat -tlnp | grep :80
# یا
sudo ss -tlnp | grep :80
```

باید nginx را ببینید.

### 4. تست Nginx:

```bash
curl http://localhost
```

اگر کار کرد، مشکل از Firewall است.

### 5. بررسی لاگ Nginx:

```bash
sudo tail -20 /var/log/nginx/error.log
```
