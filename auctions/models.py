from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.ImageField(_('Icon'), upload_to='category_icons/', null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('auctions:category_detail', kwargs={'slug': self.slug})


class Auction(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('pending', _('Pending Approval')),
        ('active', _('Active')),
        ('ended', _('Ended')),
        ('cancelled', _('Cancelled')),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='auctions')
    start_price = models.DecimalField(_('Start Price'), max_digits=10, decimal_places=2)
    current_price = models.DecimalField(_('Current Price'), max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(_('Reserve Price'), max_digits=10, decimal_places=2, null=True, blank=True)
    start_time = models.DateTimeField(_('Start Time'))
    end_time = models.DateTimeField(_('End Time'))
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    manual_status_override = models.BooleanField(_('Manual Status Override'), default=False, help_text=_('If checked, the status will not be automatically updated based on time.'))
    location = models.CharField(_('Location'), max_length=200)
    latitude = models.DecimalField(_('Latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('Longitude'), max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Auction')
        verbose_name_plural = _('Auctions')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        now = timezone.now()
        return (
            self.status == 'active' and
            self.start_time <= now and
            self.end_time > now
        )


class AuctionImage(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('Image'), upload_to='auction_images/')
    is_primary = models.BooleanField(_('Is Primary'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Auction Image')
        verbose_name_plural = _('Auction Images')


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(
        _('Amount'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Bid')
        verbose_name_plural = _('Bids')
        ordering = ['-amount']

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.auction.title}"


class AuctionAnalytics(models.Model):
    auction = models.OneToOneField(Auction, on_delete=models.CASCADE, related_name='analytics')
    views_count = models.PositiveIntegerField(_('Views Count'), default=0)
    unique_viewers = models.PositiveIntegerField(_('Unique Viewers'), default=0)
    max_bid = models.DecimalField(_('Maximum Bid'), max_digits=10, decimal_places=2, default=0)
    bids_count = models.PositiveIntegerField(_('Bids Count'), default=0)
    watchers_count = models.PositiveIntegerField(_('Watchers Count'), default=0)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Auction Analytics')
        verbose_name_plural = _('Auction Analytics')
