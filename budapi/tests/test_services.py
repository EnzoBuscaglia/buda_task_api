from unittest.mock import patch

from django.test import TestCase

from budapi.services.base import calculate_single_market_spread, get_all_market_spreads


class MarketSpreadsTestCase(TestCase):
    @patch("budapi.services.base.requests.get")
    def test_calculate_single_market_spread(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {
            "ticker": {
                "min_ask": ["851.8299999982119", "CLP"],
                "max_bid": ["850.0", "CLP"],
            }
        }
        mock_requests_get.return_value.status_code = 200
        spread, currency = calculate_single_market_spread("btc-clp")
        self.assertAlmostEqual(spread, 1.8299999982119)
        self.assertEqual(currency, "clp")

    @patch("budapi.services.base.calculate_single_market_spread")
    @patch("budapi.utils.get_every_public_market_id")
    def test_get_all_market_spreads(
        self, mock_get_every_public_market_id, mock_calculate_single_market_spread
    ):
        mock_get_every_public_market_id.return_value = ["btc-clp", "ltc-pen", "eth-clp"]
        mock_spreads = {
            "btc-clp": (250621.4699999988, "clp"),
            "ltc-pen": (4.880000000000024, "pen"),
            "eth-clp": (9514.0, "clp"),
        }

        def mock_spread_func(market_id):
            return mock_spreads.get(
                market_id, (None, None)
            )  # TODO: check mock_spreads[market_id]

        mock_calculate_single_market_spread.side_effect = mock_spread_func
        result = get_all_market_spreads()
        expected_result = [
            ("btc-clp", 250621.4699999988, "clp"),
            ("eth-clp", 9514.0, "clp"),
            ("ltc-pen", 4.880000000000024, "pen"),
        ]
        self.assertEqual(result, expected_result)
