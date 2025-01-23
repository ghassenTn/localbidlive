from django.urls import path
from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.auction_list, name='auction_list'),
    path('create/', views.auction_create, name='auction_create'),
    path('<int:pk>/', views.auction_detail, name='auction_detail'),
    path('<int:pk>/edit/', views.auction_edit, name='auction_edit'),
    path('<int:pk>/bid/', views.place_bid, name='place_bid'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('my-auctions/', views.my_auctions, name='my_auctions'),
    path('my-bids/', views.my_bids, name='my_bids'),
    
    # API endpoints
    path('api/auctions/<int:pk>/bid/', views.place_bid, name='place_bid_api'),
]
