from django.contrib import admin
from .models import Notification, NotificationLog


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'status', 'scheduled_time']
    list_filter = ['notification_type', 'status', 'scheduled_time']
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'sent_time']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'notification_type', 'title', 'message', 'status')
        }),
        ('Related Objects', {
            'fields': ('event_id', 'appointment_id')
        }),
        ('Timing', {
            'fields': ('scheduled_time', 'sent_time')
        }),
        ('Notification Channels', {
            'fields': ('notify_in_app', 'notify_email', 'notify_browser')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['notification', 'channel', 'success', 'attempt_time']
    list_filter = ['channel', 'success', 'attempt_time']
    search_fields = ['notification__title']
    readonly_fields = ['attempt_time']
