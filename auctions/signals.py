from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Auction, Bid, AuctionAnalytics


@receiver(post_save, sender=Auction)
def create_auction_analytics(sender, instance, created, **kwargs):
    """Create AuctionAnalytics when a new Auction is created."""
    if created:
        AuctionAnalytics.objects.create(auction=instance)


@receiver(post_save, sender=Bid)
def update_auction_analytics(sender, instance, created, **kwargs):
    """Update AuctionAnalytics when a new Bid is created."""
    if created:
        analytics = instance.auction.analytics
        analytics.bids_count = instance.auction.bids.count()
        analytics.max_bid = max(analytics.max_bid, instance.amount)
        analytics.save()


@receiver(pre_save, sender=Auction)
def check_auction_status(sender, instance, **kwargs):
    """Update auction status based on time unless manually overridden."""
    # Skip status update if manual override is enabled
    if instance.manual_status_override:
        return

    now = timezone.now()
    
    # Make sure we're comparing timezone-aware datetimes
    start_time = instance.start_time
    end_time = instance.end_time
    
    if not timezone.is_aware(start_time):
        start_time = timezone.make_aware(start_time)
    if not timezone.is_aware(end_time):
        end_time = timezone.make_aware(end_time)
    
    if start_time > now:
        instance.status = 'pending'
    elif end_time < now:
        instance.status = 'ended'
    elif start_time <= now <= end_time:
        instance.status = 'active'
