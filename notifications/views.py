from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Notification, NotificationPreference


@login_required
def notification_list(request):
    """Display list of user's notifications."""
    notifications = Notification.objects.filter(user=request.user)
    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications/notification_list.html', context)


@login_required
def mark_notification_read(request, pk):
    """Mark a single notification as read."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    messages.success(request, _('Notification marked as read.'))
    return redirect('notifications:notification_list')


@login_required
def mark_all_read(request):
    """Mark all notifications as read."""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, _('All notifications marked as read.'))
    return redirect('notifications:notification_list')


@login_required
def notification_preferences(request):
    """Update notification preferences."""
    preferences, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preferences.email_notifications = request.POST.get('email_notifications') == 'on'
        preferences.push_notifications = request.POST.get('push_notifications') == 'on'
        preferences.auction_start_reminder = request.POST.get('auction_start_reminder') == 'on'
        preferences.new_bid_alert = request.POST.get('new_bid_alert') == 'on'
        preferences.outbid_alert = request.POST.get('outbid_alert') == 'on'
        preferences.auction_end_reminder = request.POST.get('auction_end_reminder') == 'on'
        preferences.auction_won_notification = request.POST.get('auction_won_notification') == 'on'
        preferences.payment_notification = request.POST.get('payment_notification') == 'on'
        preferences.save()
        
        messages.success(request, _('Notification preferences updated successfully.'))
        return redirect('notifications:preferences')
    
    context = {
        'preferences': preferences,
    }
    return render(request, 'notifications/preferences.html', context)
