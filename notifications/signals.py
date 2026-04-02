from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from events.models import Event, Appointment
from .models import Notification
from .utils import create_event_notification, create_appointment_notification
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Event)
def create_event_notification_signal(sender, instance, created, **kwargs):
    """
    Signal handler to create notifications when an event is created or updated
    """
    if created:
        try:
            create_event_notification(instance)
            logger.info(f"Notification signal triggered for event: {instance.title}")
        except Exception as e:
            logger.error(f"Error creating event notification: {str(e)}")


@receiver(post_save, sender=Appointment)
def create_appointment_notification_signal(sender, instance, created, **kwargs):
    """
    Signal handler to create notifications when an appointment is created or updated
    """
    if created:
        try:
            create_appointment_notification(instance)
            logger.info(f"Notification signal triggered for appointment: {instance.attendee_name}")
        except Exception as e:
            logger.error(f"Error creating appointment notification: {str(e)}")


@receiver(post_delete, sender=Event)
def delete_event_notifications(sender, instance, **kwargs):
    """
    Signal handler to delete related notifications when an event is deleted
    """
    try:
        Notification.objects.filter(
            event_id=instance.id,
            notification_type='event'
        ).delete()
        logger.info(f"Deleted notifications for event: {instance.title}")
    except Exception as e:
        logger.error(f"Error deleting event notifications: {str(e)}")


@receiver(post_delete, sender=Appointment)
def delete_appointment_notifications(sender, instance, **kwargs):
    """
    Signal handler to delete related notifications when an appointment is deleted
    """
    try:
        Notification.objects.filter(
            appointment_id=instance.id,
            notification_type='appointment'
        ).delete()
        logger.info(f"Deleted notifications for appointment: {instance.attendee_name}")
    except Exception as e:
        logger.error(f"Error deleting appointment notifications: {str(e)}")
