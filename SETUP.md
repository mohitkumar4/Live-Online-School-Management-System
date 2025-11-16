# Live School - Quick Setup Guide

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation Steps

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

5. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

6. **Run the server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Homepage: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Initial Setup (After First Run)

### 1. Create Categories
- Go to Admin Panel → Courses → Categories
- Create categories like "Programming", "Mathematics", "Science", etc.

### 2. Create an Instructor Account
- Register a new account and select "Instructor" role
- Or change an existing user's role to "Instructor" in the admin panel

### 3. Create Your First Course
- Login as an instructor
- Click "Create Course" in the navigation
- Fill in course details and save

### 4. Add Lessons to Course
- Go to Admin Panel → Lessons → Lessons
- Create lessons for your course
- Set lesson type (Video, Text, Quiz)
- Add video URLs or upload video files
- Set lesson order

### 5. Create Quizzes (Optional)
- Go to Admin Panel → Quizzes → Quizzes
- Create a quiz for your course
- Add questions and choices
- Mark correct answers

## Key Features

### For Students:
- ✅ Browse and search courses
- ✅ Enroll in courses
- ✅ Watch video lessons
- ✅ Track learning progress
- ✅ Take quizzes and assessments
- ✅ Earn certificates upon completion
- ✅ Participate in discussions
- ✅ Rate and review courses

### For Instructors:
- ✅ Create and manage courses
- ✅ Add video/text lessons
- ✅ Create quizzes
- ✅ View enrollment statistics
- ✅ Moderate discussions
- ✅ Track student progress

### For Administrators:
- ✅ Full platform management
- ✅ User management
- ✅ Content moderation
- ✅ Analytics dashboard

## Important URLs

- Course List: `/courses/` or `/`
- Course Detail: `/courses/<slug>/`
- Dashboard: `/dashboard/`
- Admin Panel: `/admin/`
- Forum: `/forum/course/<slug>/`
- Certificates: `/certificates/`

## Notes

- All courses are free by default (can be changed)
- Media files are stored in `/media/` directory
- Static files are collected to `/staticfiles/` directory
- Database is SQLite by default (changeable in settings.py)

## Troubleshooting

1. **Static files not loading:**
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` in settings.py

2. **Media files not uploading:**
   - Create `/media/` directory in project root
   - Check file permissions

3. **Database errors:**
   - Delete `db.sqlite3` and run migrations again
   - Check database settings in settings.py

4. **Template errors:**
   - Verify all template files are in correct directories
   - Check template paths in settings.py

## Next Steps

1. Customize the look and feel by editing CSS in `/static/css/style.css`
2. Add more categories and courses
3. Configure email settings for user verification (optional)
4. Set up production database (PostgreSQL recommended)
5. Deploy to a hosting platform

## Support

For issues or questions, refer to the main README.md file or create an issue in the repository.

