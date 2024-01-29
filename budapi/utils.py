import requests
from django.conf import settings


def get_markets_ids():
    response = requests.get(f"{settings.BUDA_API_URL}/markets")
    if response.status_code == 200:
        market_ids = []
        for market in response.json().get("markets", []):
            market_id = market.get("id")
            if market_id:
                market_ids.append(market_id.lower())
        return market_ids
    else:
        print("Failed to fetch data. Status code:", response.status_code)