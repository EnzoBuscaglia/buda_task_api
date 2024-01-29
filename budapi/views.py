from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from budapi.serializers import (
    SecretKeyGetRequestSerializer,
    SingleMarketSpreadGetReponseSerializer,
    SingleMarketSpreadGetRequestSerializer,
)
from budapi.services.base import (
    calculate_every_market_spread,
    calculate_single_market_spread,
)


class SingleMarketSpread(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_serializer = SingleMarketSpreadGetRequestSerializer(
            data=request.query_params
        )
        if not request_serializer.is_valid():
            return Response(
                request_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        market_spread, spread_currency = calculate_single_market_spread(
            request_serializer.validated_data["market_id"]
        )
        if not market_spread:
            return Response(
                {"error": "External API Buda API not responding"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        response_data = {
            "market_id": request_serializer.validated_data["market_id"],
            "spread_value": market_spread,
            "trading_currency": spread_currency,
        }
        response_serializer = SingleMarketSpreadGetReponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.validated_data, status.HTTP_200_OK)
        return Response(
            response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
