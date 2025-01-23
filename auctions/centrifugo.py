from django.conf import settings
from cent import Client
import json

def get_centrifugo_client():
    """Get Centrifugo client instance."""
    return Client(settings.CENTRIFUGO_HOST, api_key=settings.CENTRIFUGO_API_KEY, timeout=settings.CENTRIFUGO_TIMEOUT)

def generate_channel_token(user_id, channel, exp=None):
    """Generate token for channel subscription."""
    from jwt import encode
    
    claims = {
        "sub": str(user_id),
        "channel": channel
    }
    if exp:
        claims["exp"] = exp
        
    return encode(
        claims,
        settings.CENTRIFUGO_SECRET,
        algorithm="HS256"
    )

def publish_to_channel(channel, data):
    """Publish data to a Centrifugo channel."""
    client = get_centrifugo_client()
    client.publish(channel, data)

def get_user_token(user):
    """Generate connection token for user."""
    from jwt import encode
    from datetime import datetime, timedelta
    
    now = datetime.utcnow()
    exp = now + timedelta(days=1)  # Token expires in 1 day
    
    claims = {
        "sub": str(user.id),
        "exp": exp,
    }
    
    return encode(
        claims,
        settings.CENTRIFUGO_SECRET,
        algorithm="HS256"
    )
