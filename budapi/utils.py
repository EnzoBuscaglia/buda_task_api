import requests
from django.conf import settings


def get_every_market_id():
    response = requests.get(f"{settings.BUDA_API_URL}/markets")
    if response.status_code == 200:
        market_ids = []
        for market in response.json().get("markets", []):
            market_id = market.get("id")
            if market_id:
                market_ids.append(market_id.lower())
        return market_ids
    return None
