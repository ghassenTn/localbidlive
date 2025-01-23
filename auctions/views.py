from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from .models import Auction, Category, Bid, AuctionImage
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .centrifugo import get_user_token, generate_channel_token, publish_to_channel
import json

def auction_list(request):
    """Display list of active and pending auctions."""
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    status_filter = request.GET.get('status', 'all')  # Default to 'all'
    
    # Base queryset excluding ended auctions
    auctions = Auction.objects.exclude(status='ended')
    
    # Apply status filter if specified
    if status_filter == 'active':
        auctions = auctions.filter(status='active')
    elif status_filter == 'pending':
        auctions = auctions.filter(status='pending')
    
    # Apply category filter if specified
    if category_id:
        auctions = auctions.filter(category_id=category_id)
    
    # Apply search filter if specified
    if search_query:
        auctions = auctions.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Order by status (active first) and start time
    auctions = auctions.order_by(
        '-status',  # 'active' comes before 'pending'
        'start_time'
    )
    
    context = {
        'auctions': auctions,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'auctions/auction_list.html', context)


@login_required
def auction_create(request):
    """Create new auction."""
    if request.method == 'POST':
        try:
            # Convert string dates to datetime objects
            start_time = timezone.make_aware(datetime.strptime(request.POST['start_time'], '%Y-%m-%dT%H:%M'))
            end_time = timezone.make_aware(datetime.strptime(request.POST['end_time'], '%Y-%m-%dT%H:%M'))
            
            # Validate dates
            if start_time <= timezone.now():
                messages.error(request, _('Start time must be in the future.'))
                return redirect('auctions:auction_create')
            
            if end_time <= start_time:
                messages.error(request, _('End time must be after start time.'))
                return redirect('auctions:auction_create')

            # Get and validate decimal fields
            try:
                start_price = Decimal(request.POST['start_price'])
                if start_price <= 0:
                    messages.error(request, _('Start price must be greater than zero.'))
                    return redirect('auctions:auction_create')
            except (InvalidOperation, ValueError):
                messages.error(request, _('Invalid start price.'))
                return redirect('auctions:auction_create')

            # Handle reserve price (optional)
            reserve_price = None
            if request.POST.get('reserve_price'):
                try:
                    reserve_price = Decimal(request.POST['reserve_price'])
                    if reserve_price < start_price:
                        messages.error(request, _('Reserve price must be greater than or equal to start price.'))
                        return redirect('auctions:auction_create')
                except (InvalidOperation, ValueError):
                    messages.error(request, _('Invalid reserve price.'))
                    return redirect('auctions:auction_create')

            # Validate coordinates
            try:
                latitude = Decimal(request.POST['latitude'])
                longitude = Decimal(request.POST['longitude'])
                if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                    messages.error(request, _('Invalid coordinates.'))
                    return redirect('auctions:auction_create')
            except (InvalidOperation, ValueError):
                messages.error(request, _('Invalid coordinates.'))
                return redirect('auctions:auction_create')
            
            # Create auction
            auction = Auction(
                seller=request.user,
                title=request.POST['title'],
                description=request.POST['description'],
                category_id=request.POST['category'],
                start_price=start_price,
                current_price=start_price,
                reserve_price=reserve_price,
                start_time=start_time,
                end_time=end_time,
                location=request.POST['location'],
                latitude=latitude,
                longitude=longitude,
            )
            auction.save()
            
            # Handle image uploads
            images = request.FILES.getlist('images')
            if not images:
                messages.error(request, _('At least one image is required.'))
                auction.delete()
                return redirect('auctions:auction_create')

            for image in images:
                AuctionImage.objects.create(
                    auction=auction,
                    image=image,
                    is_primary=not auction.images.exists()
                )
            
            messages.success(request, _('Auction created successfully.'))
            return redirect('auctions:auction_detail', pk=auction.pk)
            
        except Exception as e:
            messages.error(request, _('Invalid form data. Please check your input.'))
            return redirect('auctions:auction_create')
    
    context = {
        'categories': Category.objects.all(),
    }
    return render(request, 'auctions/auction_create.html', context)


def auction_detail(request, pk):
    """Display auction details."""
    auction = get_object_or_404(Auction, pk=pk)
    
    # Generate Centrifugo tokens
    centrifugo_token = None
    if request.user.is_authenticated:
        centrifugo_token = get_user_token(request.user)
        channel = f"auction.{auction.id}"
        channel_token = generate_channel_token(request.user.id, channel)
    
    context = {
        'auction': auction,
        'bids': auction.bids.select_related('user').order_by('-amount')[:10],
        'centrifugo_token': centrifugo_token,
    }
    return render(request, 'auctions/auction_detail.html', context)


@login_required
def auction_edit(request, pk):
    """Edit auction."""
    auction = get_object_or_404(Auction, pk=pk, seller=request.user)
    if request.method == 'POST':
        auction.title = request.POST['title']
        auction.description = request.POST['description']
        auction.category_id = request.POST['category']
        auction.reserve_price = request.POST.get('reserve_price')
        auction.location = request.POST['location']
        auction.latitude = request.POST['latitude']
        auction.longitude = request.POST['longitude']
        auction.save()
        
        messages.success(request, _('Auction updated successfully.'))
        return redirect('auctions:auction_detail', pk=auction.pk)
    
    context = {
        'auction': auction,
        'categories': Category.objects.all(),
    }
    return render(request, 'auctions/auction_edit.html', context)


@login_required
def place_bid(request, pk):
    """Place bid on auction."""
    if request.method == 'POST':
        auction = get_object_or_404(Auction, pk=pk)
        
        if auction.status != 'active':
            return JsonResponse({'error': _('This auction is not active')}, status=400)
        
        if auction.seller == request.user:
            return JsonResponse({'error': _('You cannot bid on your own auction')}, status=400)
        
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                amount = Decimal(str(data.get('amount', '0')))
            else:
                amount = Decimal(str(request.POST.get('amount', '0')))
                
            if amount <= 0:
                return JsonResponse({'error': _('Invalid bid amount')}, status=400)
        except (json.JSONDecodeError, TypeError, ValueError, InvalidOperation):
            return JsonResponse({'error': _('Invalid bid amount')}, status=400)
        
        if amount <= auction.current_price:
            return JsonResponse({'error': _('Bid must be higher than current price')}, status=400)
        
        bid = Bid.objects.create(
            auction=auction,
            user=request.user,
            amount=amount
        )
        
        # Update auction current price
        auction.current_price = amount
        auction.save()
        
        # Publish to Centrifugo
        channel = f"auction.{auction.id}"
        message = {
            'type': 'new_bid',
            'auction_id': auction.id,
            'bidder_id': request.user.id,
            'bidder_username': request.user.username,
            'amount': str(amount),
            'current_price': str(auction.current_price),
            'created_at': bid.created_at.strftime('%b %d, %Y %H:%M')
        }
        publish_to_channel(channel, message)
        
        return JsonResponse({'status': 'success'})
    return redirect('auctions:auction_detail', pk=pk)


def category_list(request):
    """Display list of categories."""
    categories = Category.objects.filter(parent=None)
    context = {
        'categories': categories,
    }
    return render(request, 'auctions/category_list.html', context)


def category_detail(request, slug):
    """Display category details and its auctions."""
    category = get_object_or_404(Category, slug=slug)
    auctions = Auction.objects.filter(
        category=category,
        status='active',
        start_time__lte=timezone.now(),
        end_time__gt=timezone.now()
    )
    context = {
        'category': category,
        'auctions': auctions,
    }
    return render(request, 'auctions/category_detail.html', context)


@login_required
def my_auctions(request):
    """Display user's auctions."""
    auctions = Auction.objects.filter(seller=request.user)
    context = {
        'auctions': auctions,
    }
    return render(request, 'auctions/my_auctions.html', context)


@login_required
def my_bids(request):
    """Display user's bids."""
    bids = Bid.objects.filter(user=request.user).select_related('auction')
    context = {
        'bids': bids,
    }
    return render(request, 'auctions/my_bids.html', context)
