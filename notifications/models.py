from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('auction_start', _('Auction Start')),
        ('new_bid', _('New Bid')),
        ('outbid', _('Outbid')),
        ('auction_end', _('Auction End')),
        ('auction_won', _('Auction Won')),
        ('payment_received', _('Payment Received')),
        ('auction_canceled', _('Auction Canceled')),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(_('Type'), max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(_('Title'), max_length=200)
    message = models.TextField(_('Message'))
    is_read = models.BooleanField(_('Is Read'), default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"


class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_notifications = models.BooleanField(_('Email Notifications'), default=True)
    push_notifications = models.BooleanField(_('Push Notifications'), default=True)
    auction_start_reminder = models.BooleanField(_('Auction Start Reminder'), default=True)
    new_bid_alert = models.BooleanField(_('New Bid Alert'), default=True)
    outbid_alert = models.BooleanField(_('Outbid Alert'), default=True)
    auction_end_reminder = models.BooleanField(_('Auction End Reminder'), default=True)
    auction_won_notification = models.BooleanField(_('Auction Won Notification'), default=True)
    payment_notification = models.BooleanField(_('Payment Notification'), default=True)

    class Meta:
        verbose_name = _('Notification Preference')
        verbose_name_plural = _('Notification Preferences')

    def __str__(self):
        return f"{self.user.username}'s notification preferences"
