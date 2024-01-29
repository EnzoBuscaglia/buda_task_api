from django.conf import settings
from rest_framework import serializers

from budapi.utils import get_markets_ids


class SecretKeyGetRequestSerializer(serializers.Serializer):
    secret = serializers.CharField(max_length=40, required=True)

    def validate_secret(self, value):
        if value != settings.BUDAPI_SECRET_KEY:
            raise serializers.ValidationError("Invalid key value")
        return value


class SingleMarketSpreadGetRequestSerializer(SecretKeyGetRequestSerializer):
    market_id = serializers.CharField(required=True, allow_blank=False)

    def validate_market_id(self, value):
        provided_market_id = value.lower()
        if provided_market_id not in get_markets_ids():
            raise serializers.ValidationError(
                "This market is not available in Buda's public API"
            )
        return provided_market_id
