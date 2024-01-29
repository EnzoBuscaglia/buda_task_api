from unittest.mock import patch

from django.test import TestCase

from budapi.utils import get_every_public_market_id


class TestBudapiUtils(TestCase):
    @patch("budapi.utils.get_every_public_market_id")
    def test_get_every_public_market_id(self, mock_get_every_public_market_id):
        mock_get_every_public_market_id.return_value = [
            "btc-clp",
            "btc-cop",
            "eth-clp",
            "eth-btc",
            "btc-pen",
            "eth-pen",
            "eth-cop",
            "bch-btc",
            "bch-clp",
            "bch-cop",
            "bch-pen",
            "btc-ars",
            "eth-ars",
            "bch-ars",
            "ltc-btc",
            "ltc-clp",
            "ltc-cop",
            "ltc-pen",
            "ltc-ars",
            "usdc-clp",
            "usdc-cop",
            "usdc-pen",
            "usdc-ars",
            "btc-usdc",
            "usdt-usdc",
        ]
        market_ids = get_every_public_market_id()
        self.assertIn("btc-clp", market_ids)
        self.assertIn("ltc-cop", market_ids)
