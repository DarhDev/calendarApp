from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import timedelta
from .models import Notification, NotificationLog
import logging

logger = logging.getLogger(__name__)


def send_email_notification(notification):
    """
    Send email notification for upcoming events/appointments
    """
    try:
        # Prepare email context
        context = {
            'user': notification.user,
            'title': notification.title,
            'message': notification.message,
            'scheduled_time': notification.scheduled_time,
        }
        
        # Render email templates
        html_message = render_to_string(
            'notifications/email_notification.html', 
            context
        )
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=notification.title,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Log successful send
        NotificationLog.objects.create(
            notification=notification,
            channel='email',
            success=True
        )
        
        logger.info(f"Email notification sent to {notification.user.email}: {notification.title}")
        return True
        
    except Exception as e:
        # Log failed send
        NotificationLog.objects.create(
            notification=notification,
            channel='email',
            success=False,
            error_message=str(e)
        )
        logger.error(f"Failed to send email notification: {str(e)}")
        return False


def create_event_notification(event, time_before_hours=1):
    """
    Create notification for an upcoming event
    
    Args:
        event: Event instance
        time_before_hours: Hours before event to notify (default: 1 hour)
    """
    from django.utils import timezone
    
    # Calculate notification time (1 hour before event by default)
    notification_time = event.start_date - timedelta(hours=time_before_hours)
    
    # Check if notification already exists to avoid duplicates
    if Notification.objects.filter(
        user=event.user,
        event_id=event.id,
        notification_type='event'
    ).exists():
        return None
    
    # Create notification
    notification = Notification.objects.create(
        user=event.user,
        notification_type='event',
        title=f"Upcoming Event: {event.title}",
        message=f"Your event '{event.title}' is scheduled for {event.start_date.strftime('%Y-%m-%d %H:%M')}",
        scheduled_time=notification_time,
        event_id=event.id,
        notify_in_app=True,
        notify_email=True
    )
    
    logger.info(f"Event notification created for {event.user.username}: {event.title}")
    return notification


def create_appointment_notification(appointment, time_before_hours=2):
    """
    Create notification for an upcoming appointment
    
    Args:
        appointment: Appointment instance
        time_before_hours: Hours before appointment to notify (default: 2 hours)
    """
    from django.utils import timezone
    
    # Calculate notification time (2 hours before appointment by default)
    notification_time = appointment.start_time - timedelta(hours=time_before_hours)
    
    # Check if notification already exists to avoid duplicates
    if Notification.objects.filter(
        user=appointment.user,
        appointment_id=appointment.id,
        notification_type='appointment'
    ).exists():
        return None
    
    # Create notification
    notification = Notification.objects.create(
        user=appointment.user,
        notification_type='appointment',
        title=f"Upcoming Appointment: {appointment.attendee_name}",
        message=f"Your appointment with {appointment.attendee_name} is scheduled for {appointment.start_time.strftime('%Y-%m-%d %H:%M')} at {appointment.location}",
        scheduled_time=notification_time,
        appointment_id=appointment.id,
        notify_in_app=True,
        notify_email=True
    )
    
    logger.info(f"Appointment notification created for {appointment.user.username}: {appointment.attendee_name}")
    return notification


def process_pending_notifications():
    """
    Process all pending notifications and send them if scheduled time has arrived
    
    Returns:
        Tuple of (sent_count, failed_count)
    """
    from django.utils import timezone
    
    current_time = timezone.now()
    
    # Get all pending notifications that are due
    pending_notifications = Notification.objects.filter(
        status='pending',
        scheduled_time__lte=current_time
    )
    
    sent_count = 0
    failed_count = 0
    
    for notification in pending_notifications:
        # Send in-app notification (always happens)
        try:
            notification.mark_as_sent()
            sent_count += 1
        except Exception as e:
            logger.error(f"Failed to process notification {notification.id}: {str(e)}")
            failed_count += 1
            continue
        
        # Send email if enabled
        if notification.notify_email and notification.user.email:
            if not send_email_notification(notification):
                failed_count += 1
    
    logger.info(f"Processed {sent_count} notifications successfully, {failed_count} failed")
    return sent_count, failed_count
