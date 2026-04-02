"""
Notifications App - Usage Examples

This file contains practical examples of how to use the notifications app
in your Django views, signals, and management commands.
"""

# ============================================================================
# EXAMPLE 1: Using Notifications in Views
# ============================================================================

from django.shortcuts import render, redirect, JsonResponse
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from notifications.utils import create_event_notification
from events.models import Event

@login_required
def create_event_example(request):
    """Example of creating an event with automatic notification"""
    if request.method == 'POST':
        # Create the event
        event = Event.objects.create(
            user=request.user,
            title=request.POST['title'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
        )
        # Notification is automatically created via signal!
        
        return redirect('event_detail', pk=event.pk)


# ============================================================================
# EXAMPLE 2: Checking User's Pending Notifications
# ============================================================================

@login_required
def dashboard_with_notifications(request):
    """Get user's pending and recent notifications"""
    # Get pending notifications
    pending_notifications = Notification.objects.filter(
        user=request.user,
        status='pending'
    ).order_by('scheduled_time')[:5]
    
    # Get unread notifications
    unread_count = Notification.objects.filter(
        user=request.user,
        status__in=['pending', 'sent']
    ).count()
    
    context = {
        'pending_notifications': pending_notifications,
        'unread_count': unread_count,
    }
    return render(request, 'dashboard.html', context)


# ============================================================================
# EXAMPLE 3: Sending Notifications Manually
# ============================================================================

from django.utils import timezone
from datetime import timedelta

def notify_user_manually(request, event_id):
    """Manually create and send a notification for an event"""
    from notifications.utils import send_email_notification
    
    event = Event.objects.get(pk=event_id, user=request.user)
    
    # Create custom notification
    notification = Notification.objects.create(
        user=request.user,
        notification_type='event',
        title=f'Reminder: {event.title}',
        message=f'Remember, your event "{event.title}" is coming up!',
        scheduled_time=timezone.now(),  # Send immediately
        event_id=event.id,
        notify_in_app=True,
        notify_email=True
    )
    
    # Send immediately
    notification.mark_as_sent()
    if notification.notify_email and request.user.email:
        send_email_notification(notification)
    
    return JsonResponse({'status': 'Notification sent!'})


# ============================================================================
# EXAMPLE 4: Getting Notifications in Templates (with AJAX)
# ============================================================================

"""
<!-- In your base template or navbar -->
<div class="notification-bell">
    <a href="{% url 'notifications:notification_list' %}">
        <i class="fas fa-bell"></i>
        <span class="badge badge-danger" id="notif-count">0</span>
    </a>
</div>

<script>
// Update notification count every 30 seconds
setInterval(function() {
    fetch('/notifications/api/unread-count/')
        .then(response => response.json())
        .then(data => {
            const count = data.unread_count;
            const badge = document.getElementById('notif-count');
            badge.textContent = count;
            badge.style.display = count > 0 ? 'block' : 'none';
        });
}, 30000);
</script>
"""


# ============================================================================
# EXAMPLE 5: Custom Notification Logic in Signals
# ============================================================================

from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import Event, Appointment
from notifications.models import Notification
from datetime import datetime, timedelta

@receiver(post_save, sender=Event)
def custom_event_notification(sender, instance, created, **kwargs):
    """Custom logic for event notifications"""
    if created:
        # Don't create notification for all-day events on weekends
        if instance.is_all_day and instance.start_date.weekday() >= 5:
            return
        
        # Create notification at different times based on event type
        if instance.category == 'meeting':
            hours_before = 0.5  # 30 minutes before meetings
        elif instance.category == 'birthday':
            hours_before = 24  # 1 day before birthdays
        else:
            hours_before = 1  # Default 1 hour
        
        notification_time = instance.start_date - timedelta(hours=hours_before)
        
        Notification.objects.create(
            user=instance.user,
            notification_type='event',
            title=f'Upcoming {instance.get_category_display()}: {instance.title}',
            message=f'Your {instance.get_category_display()} "{instance.title}" is scheduled for {instance.start_date.strftime("%Y-%m-%d %H:%M")}',
            scheduled_time=notification_time,
            event_id=instance.id,
        )


# ============================================================================
# EXAMPLE 6: Bulk Notification Management
# ============================================================================

@login_required
def manage_notifications(request):
    """Example for managing multiple notifications"""
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'mark_all_read':
            # Mark all as read
            Notification.objects.filter(
                user=request.user,
                status__in=['pending', 'sent']
            ).update(status='read')
        
        elif action == 'delete_old':
            # Delete notifications older than 30 days
            thirty_days_ago = timezone.now() - timedelta(days=30)
            Notification.objects.filter(
                user=request.user,
                created_at__lt=thirty_days_ago,
                status='read'
            ).delete()
        
        elif action == 'clear_all':
            # Delete all notifications
            if request.POST.get('confirm') == 'yes':
                Notification.objects.filter(user=request.user).delete()
    
    return redirect('notifications:notification_list')


# ============================================================================
# EXAMPLE 7: Filtering Notifications by Type
# ============================================================================

@login_required
def get_notifications_by_type(request, notification_type):
    """Get notifications filtered by type"""
    
    valid_types = ['event', 'appointment', 'reminder', 'general']
    
    if notification_type not in valid_types:
        return JsonResponse({'error': 'Invalid type'}, status=400)
    
    notifications = Notification.objects.filter(
        user=request.user,
        notification_type=notification_type
    ).order_by('-scheduled_time')
    
    data = {
        'notifications': [
            {
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'scheduled_time': n.scheduled_time.isoformat(),
                'status': n.status,
            }
            for n in notifications
        ]
    }
    
    return JsonResponse(data)


# ============================================================================
# EXAMPLE 8: Scheduling Notifications at Custom Times
# ============================================================================

def suggest_notification_time(event):
    """
    Smart function to suggest notification time based on event.
    Returns appropriate time before event.
    """
    
    time_differences = {
        'work': timedelta(hours=1),
        'personal': timedelta(hours=2),
        'meeting': timedelta(minutes=15),
        'birthday': timedelta(days=1),
        'holiday': timedelta(days=7),
        'other': timedelta(hours=1),
    }
    
    time_diff = time_differences.get(event.category, timedelta(hours=1))
    return event.start_date - time_diff


# ============================================================================
# EXAMPLE 9: Creating Bulk Notifications
# ============================================================================

from django.contrib.auth.models import User

def create_notifications_for_all_upcoming_events():
    """
    Bulk create notifications for all upcoming events
    (run periodically via management command)
    """
    from datetime import timedelta, datetime
    from django.utils import timezone
    
    future_date = timezone.now() + timedelta(days=7)
    
    events = Event.objects.filter(
        start_date__lte=future_date,
        start_date__gte=timezone.now()
    ).exclude(
        notifications__notification_type='event'
    )
    
    count = 0
    for event in events:
        notification = Notification.objects.create(
            user=event.user,
            notification_type='event',
            title=f'Upcoming: {event.title}',
            message=f'Event "{event.title}" is in {(event.start_date - timezone.now()).days} days',
            scheduled_time=event.start_date - timedelta(hours=1),
            event_id=event.id,
        )
        count += 1
    
    return count, f"Created {count} notifications"


# ============================================================================
# EXAMPLE 10: Notification Statistics
# ============================================================================

@login_required
def notification_statistics(request):
    """Get notification statistics for the user"""
    
    all_notifications = Notification.objects.filter(user=request.user)
    
    stats = {
        'total': all_notifications.count(),
        'pending': all_notifications.filter(status='pending').count(),
        'sent': all_notifications.filter(status='sent').count(),
        'read': all_notifications.filter(status='read').count(),
        'failed': all_notifications.filter(status='failed').count(),
        'by_type': {
            'events': all_notifications.filter(notification_type='event').count(),
            'appointments': all_notifications.filter(notification_type='appointment').count(),
            'reminders': all_notifications.filter(notification_type='reminder').count(),
            'general': all_notifications.filter(notification_type='general').count(),
        }
    }
    
    return JsonResponse(stats)


# ============================================================================
# EXAMPLE 11: Automatic Cleanup Management Command
# ============================================================================

"""
# Create file: notifications/management/commands/cleanup_notifications.py

from django.core.management.base import BaseCommand
from notifications.models import Notification
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Clean up old read notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete read notifications older than X days'
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)
        
        deleted_count, _ = Notification.objects.filter(
            status='read',
            created_at__lt=cutoff_date
        ).delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Deleted {deleted_count} old notifications')
        )
"""


# ============================================================================
# EXAMPLE 12: Conditional Notification Based on User Preferences
# ============================================================================

"""
# Create a UserNotificationPreferences model to your events app:

class UserNotificationPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notify_emails = models.BooleanField(default=True)
    notify_events = models.BooleanField(default=True)
    notify_appointments = models.BooleanField(default=True)
    hours_before_event = models.IntegerField(default=1)
    hours_before_appointment = models.IntegerField(default=2)

# Then in your signal handler:

@receiver(post_save, sender=Event)
def create_event_notification_with_preferences(sender, instance, created, **kwargs):
    if created:
        try:
            prefs = instance.user.usernotificationpreferences
            if not prefs.notify_events:
                return
            hours = prefs.hours_before_event
        except:
            hours = 1
        
        notification_time = instance.start_date - timedelta(hours=hours)
        Notification.objects.create(
            user=instance.user,
            notification_type='event',
            title=f'Upcoming Event: {instance.title}',
            message=f'Your event "{instance.title}" is scheduled for {instance.start_date.strftime("%Y-%m-%d %H:%M")}',
            scheduled_time=notification_time,
            event_id=instance.id,
        )
"""

print("✅ Examples loaded successfully!")
