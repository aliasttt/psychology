# رفع مشکل Gunicorn Service

## مشکل:
```
Failed at step EXEC spawning /srv/psychology_app/env/bin/gunicorn: No such file or directory
```

## علت:
مسیرها در فایل service با مسیرهای واقعی سرور مطابقت ندارد.

## راه حل:

### ویرایش فایل service:

```bash
sudo nano /etc/systemd/system/psychology_clinic.service
```

### محتوای صحیح فایل (با مسیرهای شما):

```ini
[Unit]
Description=gunicorn daemon for Psychology Clinic Django application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/root/psychology
ExecStart=/root/venv/bin/gunicorn \
          --access-logfile /var/log/gunicorn/access.log \
          --error-logfile /var/log/gunicorn/error.log \
          --workers 3 \
          --bind unix:/var/run/gunicorn/psychology_clinic.sock \
          psychology_clinic.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### تغییرات مهم:
1. `WorkingDirectory=/root/psychology` (به جای `/srv/psychology_app/app`)
2. `ExecStart=/root/venv/bin/gunicorn` (به جای `/srv/psychology_app/env/bin/gunicorn`)
3. `--bind unix:/var/run/gunicorn/psychology_clinic.sock` (به جای `/run/gunicorn`)

### بعد از ویرایش:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Restart service
sudo systemctl restart psychology_clinic.service

# بررسی وضعیت
sudo systemctl status psychology_clinic.service
```

### اگر هنوز خطا گرفتید:

بررسی کنید:
- مسیر virtual environment درست باشد: `/root/venv/bin/gunicorn`
- مسیر پروژه درست باشد: `/root/psychology`
- Gunicorn نصب شده باشد: `which gunicorn` یا `/root/venv/bin/gunicorn --version`
