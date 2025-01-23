from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Auction, Bid, AuctionImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'auction_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    def auction_count(self, obj):
        return obj.auctions.count()
    auction_count.short_description = _('Number of Auctions')

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'start_price', 'current_price', 'status', 'manual_status_override', 'created_at')
    list_filter = ('status', 'category', 'manual_status_override', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    raw_id_fields = ('seller',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('seller', 'title', 'description', 'category')
        }),
        (_('Pricing'), {
            'fields': ('start_price', 'current_price', 'reserve_price')
        }),
        (_('Timing'), {
            'fields': ('start_time', 'end_time')
        }),
        (_('Status'), {
            'fields': ('status', 'manual_status_override'),
            'description': _('Enable manual status override to prevent automatic status updates based on time.')
        }),
        (_('Location'), {
            'fields': ('location', 'latitude', 'longitude')
        }),
    )

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('auction__title', 'user__username')
    raw_id_fields = ('auction', 'user')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(AuctionImage)
class AuctionImageAdmin(admin.ModelAdmin):
    list_display = ('auction', 'image', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('auction__title',)
    raw_id_fields = ('auction',)
    ordering = ('-created_at',)
