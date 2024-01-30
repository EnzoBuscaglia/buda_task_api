import time

import requests
from django.conf import settings

from budapi.utils import get_every_public_market_id


def calculate_single_market_spread(market_id):
    for i in range(3):
        time.sleep(i * 3)
        try:
            response = requests.get(
                f"{settings.BUDA_API_URL}/markets/{market_id}/ticker"
            )
            if response.status_code == 200:
                data = response.json().get("ticker", [])
                if data:
                    return (
                        float(data["min_ask"][0]) - float(data["max_bid"][0]),
                        data["min_ask"][1].lower(),
                    )
        except Exception:
            continue
    return None, None


def get_all_market_spreads():
    all_market_ids = get_every_public_market_id()
    if all_market_ids:
        all_market_spreads_data = []
        for market_id in all_market_ids:
            spread_value, spread_currency = calculate_single_market_spread(market_id)
            if spread_value:
                all_market_spreads_data.append(
                    (market_id, spread_value, spread_currency)
                )
        return all_market_spreads_data
    return None
