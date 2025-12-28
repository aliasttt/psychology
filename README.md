# Psychology Clinic - Django Web Application

A production-ready Django web application for psychology and mental health services.

## Features

- **Home Page**: Introduction to the clinic and services
- **Blog Section**: SEO-friendly blog with categories and tags
- **Services Pages**: Detailed service descriptions with pricing and FAQs
- **Appointment System**: Online appointment request form with email notifications
- **Contact Form**: Contact page with map integration
- **Multilingual Ready**: English and Turkish language support
- **Admin Panel**: Full Django admin interface
- **Responsive Design**: Bootstrap 5 based UI
- **SEO Optimized**: Meta tags, sitemap, robots.txt, schema.org markup
- **Security**: Production-ready security settings

## Tech Stack

- Python 3.12+
- Django 5.0+
- PostgreSQL
- Gunicorn
- Nginx
- Bootstrap 5

## Quick Start (Development)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd psichlogy
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. **Setup database**
   ```bash
   # Create PostgreSQL database
   createdb psychology_db
   
   # Or use SQLite for development (change settings.py)
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Website: http://127.0.0.1:8000
    - Admin: http://127.0.0.1:8000/admin

## Project Structure

```
psichlogy/
├── psychology_clinic/      # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI configuration
├── core/                   # Core app (home, privacy, cookies)
├── blog/                   # Blog app (posts, categories, tags)
├── services/               # Services app (services, FAQs)
├── appointments/           # Appointment booking app
├── contact/               # Contact form app
├── templates/             # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── deployment/             # Deployment configurations
│   ├── gunicorn.service    # Systemd service file
│   ├── nginx.conf          # Nginx configuration
│   └── DEPLOYMENT.md       # Full deployment guide
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
└── manage.py              # Django management script
```

## Production Deployment

See [deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md) for complete step-by-step deployment instructions for Ubuntu 22.04 VPS.

Quick deployment steps:
1. Setup server (Ubuntu 22.04)
2. Install PostgreSQL, Nginx, Python
3. Configure database
4. Deploy application code
5. Setup Gunicorn service
6. Configure Nginx
7. Setup SSL with Let's Encrypt
8. Configure firewall

## Environment Variables

Required environment variables (see `env.example`):

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database credentials
- `EMAIL_*`: Email configuration for notifications
- `CSRF_TRUSTED_ORIGINS`: HTTPS origins for CSRF protection

## Database Models

- **Post**: Blog posts with categories, tags, SEO fields
- **Category**: Blog post categories
- **Tag**: Blog post tags
- **Service**: Therapy services with pricing and FAQs
- **FAQ**: Frequently asked questions linked to services
- **Appointment**: Appointment requests from clients
- **ContactMessage**: Contact form submissions

## Admin Panel

Access the admin panel at `/admin` after creating a superuser.

Features:
- Full CRUD for all models
- Rich admin interface with filters and search
- Bulk actions for appointments and messages
- Image uploads for posts and services

## Security Features

- DEBUG=False in production
- Secure cookies and sessions
- CSRF protection enabled
- XSS protection headers
- HSTS enabled
- Environment-based configuration
- No secrets in code

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For deployment issues, refer to the [deployment guide](deployment/DEPLOYMENT.md).

For application issues, check the logs:
- Gunicorn: `/var/log/gunicorn/error.log`
- Nginx: `/var/log/nginx/error.log`
- Django: `logs/django_errors.log`
