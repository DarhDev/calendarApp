from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Notification(models.Model):
    """Model for storing notifications"""
    NOTIFICATION_TYPE_CHOICES = [
        ('event', 'Event Notification'),
        ('appointment', 'Appointment Notification'),
        ('reminder', 'Reminder'),
        ('general', 'General'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Links to related objects
    event_id = models.IntegerField(null=True, blank=True)
    appointment_id = models.IntegerField(null=True, blank=True)
    
    # Notification timing
    scheduled_time = models.DateTimeField()
    sent_time = models.DateTimeField(null=True, blank=True)
    
    # Notification channels
    notify_in_app = models.BooleanField(default=True)
    notify_email = models.BooleanField(default=True)
    notify_browser = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username} ({self.status})"
    
    def mark_as_sent(self):
        """Mark notification as sent"""
        self.status = 'sent'
        self.sent_time = timezone.now()
        self.save()
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.status = 'read'
        self.save()
    
    class Meta:
        ordering = ['-scheduled_time']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['scheduled_time', 'status']),
        ]


class NotificationLog(models.Model):
    """Model to log notification sending attempts"""
    CHANNEL_CHOICES = [
        ('in_app', 'In-App'),
        ('email', 'Email'),
        ('browser', 'Browser Push'),
    ]
    
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='logs')
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    attempt_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        status = 'Success' if self.success else 'Failed'
        return f"{self.notification.title} - {self.channel} - {status}"
    
    class Meta:
        ordering = ['-attempt_time']
