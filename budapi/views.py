from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from budapi.serializers import (
    MultipleMarketSpreadGetResponseSerializer,
    SecretKeyGetRequestSerializer,
    SingleMarketSpreadGetReponseSerializer,
    SingleMarketSpreadGetRequestSerializer,
)
from budapi.services.base import calculate_single_market_spread, get_all_market_spreads


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
        if market_spread is None:
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


class AllMarketSpread(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_serializer = SecretKeyGetRequestSerializer(data=request.query_params)
        if not request_serializer.is_valid():
            return Response(
                request_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        all_market_spreads = get_all_market_spreads()
        if all_market_spreads is None:
            return Response(
                {"error": "External API Buda API not responding"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        response_data = []
        for market_id, spread_value, spread_currency in all_market_spreads:
            response_data.append(
                {
                    "market_id": market_id,
                    "spread_value": spread_value,
                    "trading_currency": spread_currency,
                }
            )
        response_serializer = MultipleMarketSpreadGetResponseSerializer(
            data={"all_markets_spread_data": response_data}
        )
        if response_serializer.is_valid():
            return Response(
                response_serializer.validated_data, status=status.HTTP_200_OK
            )
        else:
            return Response(
                response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
