from django import forms
from .models import Event, Reminder, Appointment


class EventForm(forms.ModelForm):
    """Form for creating and editing events"""
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'location', 
                  'category', 'status', 'is_all_day', 'color']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Event Description'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_all_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }


class ReminderForm(forms.ModelForm):
    """Form for creating reminders"""
    class Meta:
        model = Reminder
        fields = ['reminder_type', 'time_before', 'time_unit']
        widgets = {
            'reminder_type': forms.Select(attrs={'class': 'form-control'}),
            'time_before': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Time Value'}),
            'time_unit': forms.Select(attrs={'class': 'form-control'}),
        }


class AppointmentForm(forms.ModelForm):
    """Form for creating and editing appointments"""
    class Meta:
        model = Appointment
        fields = ['title', 'description', 'appointment_type', 'start_time', 'end_time', 
                  'location', 'status', 'attendee_name', 'attendee_email', 'attendee_phone', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Appointment Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'appointment_type': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'attendee_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Attendee Name'}),
            'attendee_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Attendee Email'}),
            'attendee_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Attendee Phone'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional Notes'}),
        }
