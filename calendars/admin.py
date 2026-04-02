# from django.contrib import admin
# from .models import Event, Reminder, Appointment


# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ['title', 'user', 'start_date', 'category', 'status']
#     list_filter = ['category', 'status', 'created_at', 'user']
#     search_fields = ['title', 'description', 'location']
#     readonly_fields = ['created_at', 'updated_at']
#     fieldsets = (
#         ('Event Information', {
#             'fields': ('user', 'title', 'description')
#         }),
#         ('Timing', {
#             'fields': ('start_date', 'end_date', 'is_all_day')
#         }),
#         ('Details', {
#             'fields': ('location', 'category', 'status', 'color')
#         }),
#         ('Metadata', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if not request.user.is_superuser:
#             qs = qs.filter(user=request.user)
#         return qs
    
#     def save_model(self, request, obj, form, change):
#         if not obj.user_id:
#             obj.user = request.user
#         super().save_model(request, obj, form, change)


# @admin.register(Reminder)
# class ReminderAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'event', 'reminder_type', 'reminder_time', 'is_sent']
#     list_filter = ['reminder_type', 'is_sent', 'created_at']
#     search_fields = ['event__title']
#     readonly_fields = ['created_at', 'reminder_time']


# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = ['title', 'user', 'start_time', 'appointment_type', 'status', 'attendee_name']
#     list_filter = ['appointment_type', 'status', 'created_at', 'user']
#     search_fields = ['title', 'attendee_name', 'attendee_email', 'location']
#     readonly_fields = ['created_at', 'updated_at']
#     fieldsets = (
#         ('Appointment Information', {
#             'fields': ('user', 'title', 'description', 'appointment_type')
#         }),
#         ('Timing & Location', {
#             'fields': ('start_time', 'end_time', 'location')
#         }),
#         ('Attendee Information', {
#             'fields': ('attendee_name', 'attendee_email', 'attendee_phone')
#         }),
#         ('Status & Notes', {
#             'fields': ('status', 'notes')
#         }),
#         ('Metadata', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if not request.user.is_superuser:
#             qs = qs.filter(user=request.user)
#         return qs
    
#     def save_model(self, request, obj, form, change):
#         if not obj.user_id:
#             obj.user = request.user
#         super().save_model(request, obj, form, change)
