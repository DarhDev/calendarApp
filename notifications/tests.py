from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from events.models import Event, Appointment
from .models import Notification
from .utils import create_event_notification, create_appointment_notification


class NotificationModelTest(TestCase):
    """Tests for Notification model"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.event = Event.objects.create(
            user=self.user,
            title='Test Event',
            start_date=timezone.now() + timedelta(hours=2),
            end_date=timezone.now() + timedelta(hours=3),
        )
    
    def test_notification_creation(self):
        """Test creating a notification"""
        notification = Notification.objects.create(
            user=self.user,
            notification_type='event',
            title='Test Notification',
            message='This is a test notification',
            scheduled_time=timezone.now() + timedelta(hours=1),
            event_id=self.event.id,
        )
        self.assertTrue(notification.id)
        self.assertEqual(notification.status, 'pending')
    
    def test_mark_as_sent(self):
        """Test marking notification as sent"""
        notification = Notification.objects.create(
            user=self.user,
            notification_type='event',
            title='Test Notification',
            message='This is a test notification',
            scheduled_time=timezone.now() + timedelta(hours=1),
        )
        notification.mark_as_sent()
        self.assertEqual(notification.status, 'sent')
        self.assertIsNotNone(notification.sent_time)
    
    def test_mark_as_read(self):
        """Test marking notification as read"""
        notification = Notification.objects.create(
            user=self.user,
            notification_type='event',
            title='Test Notification',
            message='This is a test notification',
            scheduled_time=timezone.now() + timedelta(hours=1),
        )
        notification.mark_as_read()
        self.assertEqual(notification.status, 'read')


class EventNotificationSignalTest(TestCase):
    """Tests for event notification signal"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
    
    def test_event_notification_auto_creation(self):
        """Test that notification is created when event is created"""
        event = Event.objects.create(
            user=self.user,
            title='Test Event',
            start_date=timezone.now() + timedelta(hours=2),
            end_date=timezone.now() + timedelta(hours=3),
        )
        
        # Check notification was created
        notification = Notification.objects.filter(
            user=self.user,
            event_id=event.id,
            notification_type='event'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.title, f'Upcoming Event: {event.title}')
    
    def test_appointment_notification_auto_creation(self):
        """Test that notification is created when appointment is created"""
        appointment = Appointment.objects.create(
            user=self.user,
            attendee_name='John Doe',
            start_time=timezone.now() + timedelta(hours=3),
            location='Conference Room',
        )
        
        # Check notification was created
        notification = Notification.objects.filter(
            user=self.user,
            appointment_id=appointment.id,
            notification_type='appointment'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertEqual(notification.title, f'Upcoming Appointment: {appointment.attendee_name}')


class NotificationViewTest(TestCase):
    """Tests for notification views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.client.login(username='testuser', password='password')
        
        self.notification = Notification.objects.create(
            user=self.user,
            notification_type='general',
            title='Test Notification',
            message='This is a test notification',
            scheduled_time=timezone.now() + timedelta(hours=1),
        )
    
    def test_notification_list_view(self):
        """Test notification list view"""
        response = self.client.get('/notifications/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/notification_list.html')
    
    def test_notification_detail_view(self):
        """Test notification detail view"""
        response = self.client.get(f'/notifications/{self.notification.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/notification_detail.html')
