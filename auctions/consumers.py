import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.auction_group_name = f'auction_{self.auction_id}'

        # Join auction group
        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave auction group
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        bid_amount = text_data_json['bid_amount']
        user_id = self.scope["user"].id

        # Save bid to database
        bid = await self.save_bid(user_id, bid_amount)
        
        if bid:
            # Send bid to auction group
            await self.channel_layer.group_send(
                self.auction_group_name,
                {
                    'type': 'auction_bid',
                    'bid_amount': bid_amount,
                    'user_id': user_id,
                    'timestamp': timezone.now().isoformat()
                }
            )

    async def auction_bid(self, event):
        # Send bid to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'bid',
            'bid_amount': event['bid_amount'],
            'user_id': event['user_id'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def save_bid(self, user_id, amount):
        # Import here to avoid circular import
        from .models import Bid, Auction
        try:
            auction = Auction.objects.get(id=self.auction_id)
            if auction.is_active and amount > auction.current_price:
                bid = Bid.objects.create(
                    auction=auction,
                    user_id=user_id,
                    amount=amount
                )
                auction.current_price = amount
                auction.save()
                return bid
        except Auction.DoesNotExist:
            pass
        return None
