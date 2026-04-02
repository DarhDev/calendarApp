# Notifications App Documentation

## Overview
The Notifications app is a Django application that automatically creates and manages notifications for upcoming events and appointments in the Calendar Pro application.

## Features
- **Automatic Notification Creation**: Notifications are automatically created when events or appointments are created
- **Multiple Notification Channels**: Support for in-app, email, and browser notifications
- **Scheduled Notifications**: Notifications are sent at specified times before events/appointments
- **Notification Management**: Users can view, mark as read, and delete notifications
- **Notification Logging**: All notification attempts are logged for debugging

## Configuration

### 1. Add to INSTALLED_APPS
The app should already be added to `INSTALLED_APPS` in `myproject/settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'notifications',
]
```

### 2. Email Configuration
Configure email settings in `myproject/settings.py`:

```python
# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### 3. URL Configuration
URLs should already be included in `myproject/urls.py`:

```python
urlpatterns = [
    # ... other urls
    path('notifications/', include('notifications.urls', namespace="notifications")),
]
```

## Database Migration

Run migrations to create the notification tables:

```bash
python manage.py migrate
```

## Models

### Notification Model
Stores notification information:
- `user`: Foreign key to the User model
- `notification_type`: Type of notification (event, appointment, reminder, general)
- `title`: Notification title
- `message`: Notification message
- `status`: Current status (pending, sent, read, failed)
- `event_id`: ID of related event (if applicable)
- `appointment_id`: ID of related appointment (if applicable)
- `scheduled_time`: When the notification should be sent
- `sent_time`: When the notification was actually sent
- `notify_in_app`: Whether to show in-app notification
- `notify_email`: Whether to send email notification
- `notify_browser`: Whether to send browser push notification

### NotificationLog Model
Logs all notification sending attempts:
- `notification`: Foreign key to Notification
- `channel`: Channel used (in_app, email, browser)
- `success`: Whether the send was successful
- `error_message`: Error message if failed
- `attempt_time`: When the send was attempted

## Views

### Available Views:
- `notification:notification_list` - List all notifications
- `notification:notification_detail` - View notification details
- `notification:mark_as_read` - Mark notification as read
- `notification:delete_notification` - Delete a notification
- `notification:mark_all_as_read` - Mark all notifications as read
- `notification:unread_count` - AJAX endpoint for unread count
- `notification:recent_notifications` - AJAX endpoint for recent notifications

## Management Commands

### send_notifications
Process pending notifications and send them:

```bash
# Basic usage
python manage.py send_notifications

# Verbose output
python manage.py send_notifications --verbose
```

This command should be run periodically (e.g., every minute via cron or APScheduler).

## Automatic Notification Creation

### Event Notifications
When an event is created, a notification is automatically scheduled for 1 hour before the event start time.

```python
from events.models import Event
# When you create or save an Event instance
event = Event.objects.create(
    user=user,
    title="Team Meeting",
    start_date=datetime.now() + timedelta(hours=2),
    end_date=datetime.now() + timedelta(hours=3),
)
# A notification is automatically created for 1 hour before
```

### Appointment Notifications
When an appointment is created, a notification is automatically scheduled for 2 hours before the appointment start time.

```python
from events.models import Appointment
# When you create or save an Appointment instance
appointment = Appointment.objects.create(
    user=user,
    attendee_name="John Doe",
    start_time=datetime.now() + timedelta(hours=3),
    location="Conference Room A",
)
# A notification is automatically created for 2 hours before
```

## Setting Up Periodic Task Execution

### Option 1: Using Cron (Linux/macOS)

Add this line to your crontab (runs every minute):

```bash
* * * * * cd /path/to/project && python manage.py send_notifications
```

### Option 2: Using APScheduler

Install APScheduler:

```bash
pip install django-apscheduler
```

Create a management command or use Celery to run `send_notifications` periodically.

### Option 3: Using Celery + Beat

Install Celery:

```bash
pip install celery celery-beat
```

Create a `tasks.py` file in the notifications app:

```python
from celery import shared_task
from .utils import process_pending_notifications

@shared_task
def send_pending_notifications():
    return process_pending_notifications()
```

Then configure Celery Beat to run this task every minute.

## Usage Examples

### Manually Creating a Notification

```python
from notifications.models import Notification
from django.utils import timezone
from datetime import timedelta

notification = Notification.objects.create(
    user=request.user,
    notification_type='general',
    title='Your Custom Notification',
    message='This is a custom notification message',
    scheduled_time=timezone.now() + timedelta(hours=1),
    notify_in_app=True,
    notify_email=True
)
```

### Getting Unread Notifications

```python
from notifications.models import Notification

unread = Notification.objects.filter(
    user=request.user,
    status__in=['pending', 'sent']
)
```

### Processing Notifications Manually

```python
from notifications.utils import process_pending_notifications

sent_count, failed_count = process_pending_notifications()
print(f"Sent: {sent_count}, Failed: {failed_count}")
```

## Frontend Integration

### Display Notification Bell with Count

```html
<a href="{% url 'notifications:notification_list' %}">
    <i class="fas fa-bell"></i>
    <span id="notification-count" class="badge badge-danger">
        {{ unread_count }}
    </span>
</a>
```

### Update Count via AJAX

```javascript
fetch('/notifications/api/unread-count/')
    .then(response => response.json())
    .then(data => {
        document.getElementById('notification-count').textContent = data.unread_count;
    });
```

### Get Recent Notifications via AJAX

```javascript
fetch('/notifications/api/recent/')
    .then(response => response.json())
    .then(data => {
        console.log(data.notifications);
    });
```

## Templates

### notification_list.html
Main page to view all notifications with filtering options.

### notification_detail.html
Detailed view of a single notification.

### email_notification.html
Email template sent to users.

## Signals

The app uses Django signals to automatically create notifications:

- `post_save` on Event model: Creates event notification
- `post_save` on Appointment model: Creates appointment notification
- `post_delete` on Event model: Deletes related notifications
- `post_delete` on Appointment model: Deletes related notifications

## Settings Recommendations

Add these to your Django settings for optimal notification functionality:

```python
# Notifications
NOTIFICATION_EVENT_HOURS_BEFORE = 1  # Hours before event to notify
NOTIFICATION_APPOINTMENT_HOURS_BEFORE = 2  # Hours before appointment to notify

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@calendarpro.com'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'notifications.log',
        },
    },
    'loggers': {
        'notifications': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Troubleshooting

### Notifications Not Being Sent
1. Check if the management command is running: `python manage.py send_notifications --verbose`
2. Verify email settings are configured correctly
3. Check notification logs in the database
4. Verify that notifications exist in the database with status='pending'

### Email Not Being Sent
1. Test email configuration with Django shell:
   ```python
   from django.core.mail import send_mail
   send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
   ```
2. Check email provider allows your app to send emails
3. Check firewall/security group allows SMTP port (usually 587)

### Notifications Not Created
1. Verify signals are registered (check `apps.py` `ready()` method)
2. Check Event/Appointment model save log
3. Verify user has email address set
