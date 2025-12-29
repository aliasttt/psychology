# راه‌اندازی دیتابیس PostgreSQL

## دستورات SQL برای اجرا در psql

بعد از اینکه دستور `sudo -u postgres psql` را اجرا کردید، این دستورات را یکی یکی اجرا کنید:

```sql
-- 1. ایجاد دیتابیس
CREATE DATABASE psychology_db;

-- 2. ایجاد کاربر (رمز عبور را تغییر دهید!)
CREATE USER psychology_user WITH PASSWORD 'رمز_عبور_قوی_اینجا';

-- 3. تنظیم کدگذاری UTF-8
ALTER ROLE psychology_user SET client_encoding TO 'utf8';

-- 4. تنظیم ایزولیشن تراکنش
ALTER ROLE psychology_user SET default_transaction_isolation TO 'read committed';

-- 5. تنظیم منطقه زمانی
ALTER ROLE psychology_user SET timezone TO 'Europe/Istanbul';

-- 6. اعطای دسترسی به دیتابیس
GRANT ALL PRIVILEGES ON DATABASE psychology_db TO psychology_user;

-- 7. اتصال به دیتابیس و اعطای دسترسی به schema
\c psychology_db

-- 8. اعطای دسترسی به schema public
GRANT ALL ON SCHEMA public TO psychology_user;

-- 9. اعطای دسترسی پیش‌فرض به جداول
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO psychology_user;

-- 10. اعطای دسترسی پیش‌فرض به sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO psychology_user;

-- 11. خروج از psql
\q
```

## مثال کامل (کپی و پیست کنید):

```sql
CREATE DATABASE psychology_db;
CREATE USER psychology_user WITH PASSWORD 'MySecurePassword123!';
ALTER ROLE psychology_user SET client_encoding TO 'utf8';
ALTER ROLE psychology_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE psychology_user SET timezone TO 'Europe/Istanbul';
GRANT ALL PRIVILEGES ON DATABASE psychology_db TO psychology_user;
\c psychology_db
GRANT ALL ON SCHEMA public TO psychology_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO psychology_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO psychology_user;
\q
```

## نکات مهم:

1. **رمز عبور قوی انتخاب کنید**: به جای `MySecurePassword123!` یک رمز عبور قوی و امن بگذارید
2. **رمز عبور را یادداشت کنید**: این رمز را در فایل `.env` استفاده خواهید کرد
3. **بعد از اجرا**: فایل `.env` را با اطلاعات دیتابیس پر کنید

## بررسی اتصال:

بعد از خروج از psql، می‌توانید اتصال را تست کنید:

```bash
psql -U psychology_user -d psychology_db -h localhost
```

یا:

```bash
sudo -u postgres psql -c "\l" | grep psychology_db
```
