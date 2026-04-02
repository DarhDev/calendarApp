from django import forms
from .models import Notification


class NotificationForm(forms.ModelForm):
    """Form for creating and editing notifications"""
    
    class Meta:
        model = Notification
        fields = ['title', 'message', 'notification_type', 'scheduled_time', 'notify_in_app', 'notify_email']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notification title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notification message', 'rows': 4}),
            'notification_type': forms.Select(attrs={'class': 'form-control'}),
            'scheduled_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notify_in_app': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
