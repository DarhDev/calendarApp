from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Notification views
    path('', views.notification_list, name='notification_list'),
    path('<int:pk>/', views.notification_detail, name='notification_detail'),

    
    # AJAX endpoints
    path('<int:pk>/mark-as-read/', views.mark_notification_as_read, name='mark_as_read'),
    path('<int:pk>/delete/', views.delete_notification, name='delete_notification'),
    path('api/unread-count/', views.get_unread_count, name='unread_count'),
    path('api/recent/', views.get_recent_notifications, name='recent_notifications'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
]
