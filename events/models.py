from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


class Event(models.Model):
    """Model for calendar events"""
    CATEGORY_CHOICES = [
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('meeting', 'Meeting'),
        ('birthday', 'Birthday'),
        ('holiday', 'Holiday'),
        ('other', 'Other'),
    ]

    COLOR_CHOICES = [
        ('#3498db', 'Blue'),
        ('#e74c3c', 'Red'),
        ('#2ecc71', 'Green'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    is_all_day = models.BooleanField(default=False)
    color = models.CharField(
        max_length=7, 
        choices=COLOR_CHOICES,
        default='#3498db',
        help_text='Color in hex format (e.g., #3498db)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date.")
    
    def __str__(self):
        return f"{self.title} - {self.start_date.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['start_date']
        indexes = [
            models.Index(fields=['user', 'start_date']),
        ]


class Reminder(models.Model):
    """Model for reminders associated with events"""
    REMINDER_TYPE_CHOICES = [
        ('email', 'Email'),
        ('notification', 'Notification'),
        ('sms', 'SMS'),
    ]
    
    TIME_UNIT_CHOICES = [
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES, default='notification')
    time_before = models.PositiveIntegerField()
    time_unit = models.CharField(max_length=20, choices=TIME_UNIT_CHOICES, default='minutes')
    reminder_time = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_reminder_time(self):
        """Calculate when the reminder should be sent"""
        event = self.event
        time_diff = {
            'minutes': datetime.timedelta(minutes=self.time_before),
            'hours': datetime.timedelta(hours=self.time_before),
            'days': datetime.timedelta(days=self.time_before),
        }
        return event.start_date - time_diff[self.time_unit]
    
    def save(self, *args, **kwargs):
        if not self.reminder_time:
            self.reminder_time = self.calculate_reminder_time()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_reminder_type_display()} for {self.event.title} ({self.time_before} {self.time_unit})"
    
    class Meta:
        ordering = ['reminder_time']


class Appointment(models.Model):
    """Model for booking appointments"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('meeting', 'Meeting'),
        ('checkup', 'Check-up'),
        ('service', 'Service'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='meeting')
    start_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    attendee_name = models.CharField(max_length=200, blank=True, null=True)
    attendee_email = models.EmailField(blank=True, null=True)
    attendee_phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        super().clean()
        if self.start_time and self.start_time < timezone.now():
            raise ValidationError({
                "start_time": "Appointment time cannot be in the past."
            })
        
    def __str__(self):
        return f"{self.attendee_name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['user', 'start_time']),
        ]
