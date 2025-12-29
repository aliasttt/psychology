#!/bin/bash
# Script to fix gunicorn service file

cat > /tmp/psychology_clinic.service << 'EOF'
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
EOF

sudo cp /tmp/psychology_clinic.service /etc/systemd/system/psychology_clinic.service
sudo systemctl daemon-reload
sudo systemctl restart psychology_clinic.service
sudo systemctl status psychology_clinic.service
