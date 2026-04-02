# Notifications App - Quick Setup Guide

## ✅ Installation Completed

Your notification system has been successfully installed and configured! Here's what was set up:

### What's Included

1. **Notification Models**
   - `Notification` - Stores notifications for events/appointments
   - `NotificationLog` - Tracks all notification sending attempts

2. **Automatic Notification Creation**
   - Automatically creates notifications when you create events or appointments
   - Events: Notification 1 hour before event starts
   - Appointments: Notification 2 hours before appointment starts

3. **Views & Templates**
   - Notification list page: `/notifications/`
   - Notification detail page: `/notifications/<id>/`
   - Responsive UI with filtering and management features

4. **Management Command**
   - `python manage.py send_notifications` - Process and send pending notifications

5. **Admin Interface**
   - Full admin integration at `/admin/notifications/`

## 🚀 Getting Started

### 1. Run the Development Server
```bash
cd "c:\Users\techn\Desktop\dev\examplevibe\django projects"
python manage.py runserver
```

### 2. Create Test Data
- Go to your calendar
- Create a new event or appointment
- A notification will automatically be created!

### 3. View Notifications
- Visit: `http://localhost:8000/notifications/`
- See all notifications for upcoming events/appointments

### 4. Process Notifications
To send pending notifications:
```bash
python manage.py send_notifications --verbose
```

## 📧 Email Configuration (Optional)

To enable email notifications, update your `settings.py`:

```python
# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

## ⏰ Automatic Notification Sending (Production)

For production, set up periodic execution of the management command:

### Option 1: Using Windows Task Scheduler
```
Program: C:\Users\techn\Desktop\dev\examplevibe\.venv\Scripts\python.exe
Arguments: manage.py send_notifications
Start in: C:\Users\techn\Desktop\dev\examplevibe\django projects\
Schedule: Run every minute
```

### Option 2: Using Cron (Linux/macOS)
```bash
* * * * * cd /path/to/project && python manage.py send_notifications
```

### Option 3: Using Celery (Recommended for Production)
```bash
pip install celery
# Configure Celery Beat for periodic tasks
```

## 📱 Features Overview

### For Users:
- ✅ View all upcoming notifications
- ✅ Filter by status (All, Unread, Pending, Read)
- ✅ Mark notifications as read
- ✅ Delete notifications
- ✅ Get email reminders for events/appointments

### For Developers:
- ✅ Automatic signal-based creation
- ✅ Flexible notification types
- ✅ Multiple notification channels (in-app, email, browser)
- ✅ Comprehensive logging
- ✅ Full admin interface
- ✅ AJAX API endpoints

## 🔗 Key URLs

| Page | URL |
|------|-----|
| Notifications List | `/notifications/` |
| Notification Detail | `/notifications/<id>/` |
| Mark as Read | `/notifications/<id>/mark-as-read/` (POST) |
| Delete | `/notifications/<id>/delete/` (POST) |
| Unread Count API | `/notifications/api/unread-count/` |
| Recent Notifications API | `/notifications/api/recent/` |
| Admin | `/admin/notifications/` |

## 🧪 Testing

Run the test suite:
```bash
python manage.py test notifications
```

## 📊 Customization

### Change Notification Timing
Edit `notifications/utils.py`:

```python
def create_event_notification(event, time_before_hours=1):  # Change 1 to desired hours
    ...

def create_appointment_notification(appointment, time_before_hours=2):  # Change 2 to desired hours
    ...
```

### Customize Email Template
Edit `notifications/templates/notifications/email_notification.html`

### Change Notification Status Choices
Edit `Notification.STATUS_CHOICES` in `notifications/models.py`

## 🐛 Troubleshooting

### Notifications not showing up?
1. Check if notifications exist: Visit `/admin/notifications/notification/`
2. Verify the scheduled_time is in the past
3. Run: `python manage.py send_notifications --verbose`

### Emails not sending?
1. Test email config in Django shell:
   ```python
   python manage.py shell
   >>> from django.core.mail import send_mail
   >>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
   ```
2. Check email credentials in settings.py
3. Check firewall allows SMTP port 587

### Signals not working?
1. Verify `notifications/apps.py` has `ready()` method
2. Check that 'notifications' is in INSTALLED_APPS
3. Restart Django development server

## 📚 Full Documentation
See `notifications/README.md` for complete documentation.

## 🎉 You're All Set!

Your notification system is ready to use. Create an event or appointment to see it in action!

For any issues or customization needs, refer to the README.md or SKILL.md files.
