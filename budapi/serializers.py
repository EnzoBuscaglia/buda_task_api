from django.conf import settings
from rest_framework import serializers

from budapi.utils import get_every_public_market_id


class SecretKeyGetRequestSerializer(serializers.Serializer):
    secret = serializers.CharField(max_length=40, required=True)

    def validate_secret(self, value):
        if value != settings.BUDAPI_SECRET_KEY:
            raise serializers.ValidationError("Invalid key value")
        return value


class SingleMarketSpreadGetRequestSerializer(SecretKeyGetRequestSerializer):
    market_id = serializers.CharField(required=True, allow_blank=False)

    def validate_market_id(self, value):
        lower_market_id = value.lower()
        if lower_market_id not in get_every_public_market_id():
            raise serializers.ValidationError(
                "This market is not available in Buda's public API"
            )
        return lower_market_id


class SingleMarketSpreadGetReponseSerializer(serializers.Serializer):
    market_id = serializers.CharField(allow_null=False)
    spread_value = serializers.FloatField(allow_null=False)
    trading_currency = serializers.CharField(allow_null=False)


class MultipleMarketSpreadGetResponseSerializer(serializers.Serializer):
    all_markets_spread_data = serializers.ListField(
        child=SingleMarketSpreadGetReponseSerializer()
    )


class SingleMarketSpreadPostRequestSerializer(SingleMarketSpreadGetRequestSerializer):
    alert_spread = serializers.FloatField(required=True)
    trading_currency = serializers.CharField(required=True, max_length=50)

    def validate_trading_currency(self, value):
        market_id = self.initial_data.get("market_id", "")
        lower_trading_currency = value.lower()
        if "-" in market_id:
            if lower_trading_currency != market_id.split("-", 1)[1]:
                raise serializers.ValidationError(
                    "Invalid trading currency for the given market"
                )
            return lower_trading_currency
        raise serializers.ValidationError("Invalid market_id format")
