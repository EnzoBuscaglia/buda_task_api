import requests
from django.conf import settings

from budapi.utils import get_every_market_id


def calculate_single_market_spread(market_id):
    url = f"{settings.BUDA_API_URL}/markets/{market_id}/ticker"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("ticker", [])
        if data:
            return (
                float(data["min_ask"][0]) - float(data["max_bid"][0]),
                data["min_ask"][1],
            )
    return None, None
