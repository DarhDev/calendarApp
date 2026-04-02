from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Notification
import logging

logger = logging.getLogger(__name__)


@login_required(login_url='admin:login')
def notification_list(request):
    """View to list all notifications for the logged-in user"""
    # Get filter parameter
    status_filter = request.GET.get('status', 'all')
    
    # Base query
    notifications = Notification.objects.filter(user=request.user)
    
    # Apply status filter
    if status_filter == 'unread':
        notifications = notifications.filter(Q(status='pending') | Q(status='sent'))
    elif status_filter == 'read':
        notifications = notifications.filter(status='read')
    elif status_filter == 'pending':
        notifications = notifications.filter(status='pending')
    
    # Count unread notifications
    unread_count = Notification.objects.filter(
        user=request.user,
        status__in=['pending', 'sent']
    ).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
        'status_filter': status_filter,
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required(login_url='admin:login')
def notification_detail(request, pk):
    """View to display notification details"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    
    # Mark as read when viewing
    if notification.status != 'read':
        notification.mark_as_read()
    
    context = {'notification': notification}
    return render(request, 'notifications/notification_detail.html', context)


@login_required(login_url='admin:login')
@require_http_methods(["POST"])
def mark_notification_as_read(request, pk):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('notifications:notification_list')


@login_required(login_url='admin:login')
@require_http_methods(["POST"])
def delete_notification(request, pk):
    """Delete a notification"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('notifications:notification_list')


@login_required(login_url='admin:login')
def get_unread_count(request):
    """AJAX endpoint to get unread notification count"""
    unread_count = Notification.objects.filter(
        user=request.user,
        status__in=['pending', 'sent']
    ).count()
    
    return JsonResponse({
        'unread_count': unread_count
    })


@login_required(login_url='admin:login')
def get_recent_notifications(request):
    """AJAX endpoint to get recent notifications"""
    try:
        # Get limit from query parameter, default to 5
        limit = int(request.GET.get('limit', 5))
        
        # Safety check: max 50 notifications
        limit = min(limit, 50) if limit > 0 else 5
        
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-scheduled_time')[:limit]
        
        notifications_data = [
            {
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'type': n.notification_type,
                'status': n.status,
                'scheduled_time': n.scheduled_time.isoformat(),
            }
            for n in notifications
        ]
        
        return JsonResponse({
            'success': True,
            'notifications': notifications_data,
            'count': len(notifications_data)
        })
    except Exception as e:
        import traceback
        logger.error(f"Error in get_recent_notifications: {str(e)}\n{traceback.format_exc()}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'notifications': []
        }, status=400)


@login_required(login_url='admin:login')
@require_http_methods(["POST"])
def mark_all_as_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(
        user=request.user,
        status__in=['pending', 'sent']
    ).update(status='read')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('notifications:notification_list')
