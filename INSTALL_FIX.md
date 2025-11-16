# Installation Fix for Python 3.13

## Issues Fixed:
1. **Pillow compatibility**: Updated to Pillow 11.0.0+ which supports Python 3.13
2. **Decouple optional**: Made python-decouple optional in settings.py

## Installation Steps:

### Option 1: Install All Packages (Recommended)
```bash
pip install -r requirements.txt
```

### Option 2: Install Core Packages First (If Option 1 Fails)
Install essential packages first, then optional ones:

```bash
# Core Django packages
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.0 python-decouple==3.8

# Image processing
pip install Pillow

# Additional packages
pip install django-filter==23.5 django-ckeditor==6.7.0 django-taggit==5.0.0 whitenoise==6.6.0
```

### Option 3: Install Without Optional Packages
If you're having issues with all packages, you can start with just the essentials:

```bash
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.0 Pillow django-filter python-decouple whitenoise
```

Then install others as needed:
```bash
pip install django-ckeditor django-taggit
```

### Option 4: Use Latest Versions
If you continue having issues, try installing without version pins:

```bash
pip install Django djangorestframework django-cors-headers Pillow django-filter python-decouple django-ckeditor django-taggit whitenoise
```

## After Installation:

1. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Run server:**
   ```bash
   python manage.py runserver
   ```

## Notes:
- **Removed packages**: Removed `celery`, `redis`, `channels`, and `channels-redis` from requirements as they're optional for basic functionality
- **Decouple is optional**: The settings.py now works even if python-decouple is not installed
- **Pillow**: Updated to version 11.0.0+ which has better Python 3.13 support

If you need the removed packages (celery, redis, channels) for advanced features, install them separately:
```bash
pip install celery redis channels channels-redis
```

