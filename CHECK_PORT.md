# بررسی پورت 80

## بررسی‌ها:

### 1. بررسی listen کردن Nginx:

```bash
sudo ss -tlnp | grep :80
# یا
sudo lsof -i :80
```

باید nginx را ببینید.

### 2. بررسی از خارج:

```bash
# از سرور خودتان
curl -I http://141.98.51.168
```

### 3. بررسی firewall از provider:

بعضی VPS providers (مثل DigitalOcean, AWS) firewall خودشان دارند که باید از panel تنظیم شود.

### 4. بررسی iptables:

```bash
sudo iptables -L -n | grep 80
```

### 5. تست از localhost:

```bash
curl http://localhost
curl http://127.0.0.1
```

اگر این کار کرد، مشکل از firewall provider است.
