from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from auctions.models import Bid, Auction
from .models import Notification


@receiver(post_save, sender=Bid)
def create_bid_notifications(sender, instance, created, **kwargs):
    """Create notifications when a new bid is placed."""
    if created:
        auction = instance.auction
        content_type = ContentType.objects.get_for_model(Auction)

        # Notify the seller
        Notification.objects.create(
            user=auction.seller,
            notification_type='new_bid',
            title=f'New bid on {auction.title}',
            message=f'A new bid of ${instance.amount} has been placed on your auction.',
            content_type=content_type,
            object_id=auction.id
        )

        # Notify the previous highest bidder that they've been outbid
        previous_highest_bid = Bid.objects.filter(
            auction=auction,
            created_at__lt=instance.created_at
        ).exclude(user=instance.user).first()

        if previous_highest_bid:
            Notification.objects.create(
                user=previous_highest_bid.user,
                notification_type='outbid',
                title=f'Outbid on {auction.title}',
                message=f'Someone has placed a higher bid of ${instance.amount} on this auction.',
                content_type=content_type,
                object_id=auction.id
            )
