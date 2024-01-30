import json
from datetime import date
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from model.models import MarketSpreadAlert


class ToBudaAPISingleMarketSpreadTestCase(TestCase):
    def setUp(self):
        MarketSpreadAlert.objects.create(
            market_id="ltc-btc", alert_spread=682.5100002, trading_currency="clp"
        )

    def test_invalid_api_secret(self):
        data = {
            "market_id": "btc-clp",
            "secret": "fefefe",
        }
        response = self.client.get("/api/tobuda/", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid key value", str(response.data))

    def test_missing_market_id(self):
        data = {}
        response = self.client.get("/api/tobuda/", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("This field is required", str(response.data))

    @patch("budapi.serializers.get_every_public_market_id")
    def test_unavailable_market_id(self, mock_get_every_public_market_id):
        mock_get_every_public_market_id.return_value = ["btc-clp", "ltc-pen", "eth-clp"]
        data = {
            "market_id": "dodge-clp",
            "secret": settings.BUDAPI_SECRET_KEY,
        }
        response = self.client.get("/api/tobuda/", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "This market is not available in Buda's public API", str(response.data)
        )

    @patch("budapi.views.calculate_single_market_spread")
    @patch("budapi.serializers.get_every_public_market_id")
    def test_valid_single_market_spread_request(
        self, mock_get_every_public_market_id, mock_calculate_single_market_spread
    ):
        mock_get_every_public_market_id.return_value = ["btc-clp"]
        mock_calculate_single_market_spread.return_value = (1234.56, "clp")
        data = {
            "market_id": "btc-clp",
            "secret": settings.BUDAPI_SECRET_KEY,
        }
        response = self.client.get("/api/tobuda/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "market_id": "btc-clp",
                "spread_value": 1234.56,
                "trading_currency": "clp",
            },
        )

    @patch("budapi.views.calculate_single_market_spread")
    @patch("budapi.serializers.get_every_public_market_id")
    def test_external_api_failure(
        self, mock_get_every_public_market_id, mock_calculate_single_market_spread
    ):
        mock_get_every_public_market_id.return_value = ["usdc-clp"]
        mock_calculate_single_market_spread.return_value = (None, None)
        data = {
            "market_id": "usdc-clp",
            "secret": settings.BUDAPI_SECRET_KEY,
        }
        response = self.client.get("/api/tobuda/", data, format="json")
        self.assertEqual(response.status_code, 502)
        self.assertIn("External Buda API not responding", str(response.data))

    @patch("budapi.serializers.get_every_public_market_id")
    def test_create_alert_spread(self, mock_get_every_public_market_id):
        mock_get_every_public_market_id.return_value = ["ltc-clp"]
        data = {
            "market_id": "ltc-clp",
            "alert_spread": 682.5100002,
            "trading_currency": "clp",
            "secret": settings.BUDAPI_SECRET_KEY,
        }
        response = self.client.post("/api/tobuda/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(MarketSpreadAlert.objects.filter(market_id="ltc-clp").exists())

    @patch("budapi.serializers.get_every_public_market_id")
    def test_update_alert_spread(self, mock_get_every_public_market_id):
        mock_get_every_public_market_id.return_value = ["ltc-btc"]
        data = {
            "market_id": "ltc-btc",
            "alert_spread": 1512.2,
            "trading_currency": "btc",
            "secret": settings.BUDAPI_SECRET_KEY,
        }
        response = self.client.post("/api/tobuda/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            MarketSpreadAlert.objects.filter(market_id="ltc-btc")[0].alert_spread,
            data["alert_spread"],
        )


class ToBudaAPISingleMarketPollSpreadTestCase(TestCase):
    def setUp(self):
        MarketSpreadAlert.objects.create(
            market_id="btc-usdc", alert_spread=485.160000035, trading_currency="usdc"
        )

    @patch("budapi.views.calculate_single_market_spread")
    @patch("budapi.serializers.get_every_public_market_id")
    def test_current_spread_vs_spread_alert(
        self, mock_get_every_public_market_id, mock_calculate_single_market_spread
    ):
        mock_get_every_public_market_id.return_value = ["btc-usdc"]
        mock_calculate_single_market_spread.return_value = (488.123800002, "usdc")
        data = {
            "market_id": "btc-usdc",
            "secret": settings.BUDAPI_SECRET_KEY,
        }
        response = self.client.get("/api/tobuda/poll/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())


class ToBudaAPIAllMarketsSpreadTestCase(TestCase):

    @patch("budapi.views.get_all_market_spreads")
    def test_current_spread_vs_spread_alert(
        self,
        mock_get_all_market_spreads,
    ):
        mock_get_all_market_spreads.return_value = [
            ("btc-pen", 4798.34, "pen"),
            ("eth-pen", 136.41, "pen"),
        ]
        expected_api_response = {
            "all_markets_spread_data": [
                {
                    "market_id": "btc-pen",
                    "spread_value": 4798.34,
                    "trading_currency": "pen",
                },
                {
                    "market_id": "eth-pen",
                    "spread_value": 136.41,
                    "trading_currency": "pen",
                },
            ]
        }
        data = {"secret": settings.BUDAPI_SECRET_KEY}
        response = self.client.get("/api/tobuda/all/", data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_api_response, response.json())
