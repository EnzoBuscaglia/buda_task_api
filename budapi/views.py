from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from budapi.serializers import (
    MultipleMarketSpreadGetResponseSerializer,
    SecretKeyGetRequestSerializer,
    SingleMarketSpreadGetReponseSerializer,
    SingleMarketSpreadGetRequestSerializer,
    SingleMarketSpreadPostRequestSerializer,
)
from budapi.services.base import calculate_single_market_spread, get_all_market_spreads
from model.models import MarketSpreadAlert


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
                {"error": "External Buda API not responding"},
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

    def post(self, request):
        request_serializer = SingleMarketSpreadPostRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(
                request_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        alert_spread, alert_spread_created = MarketSpreadAlert.objects.update_or_create(
            market_id=request_serializer.validated_data["market_id"],
            defaults={
                "alert_spread": request_serializer.validated_data["alert_spread"],
                "trading_currency": request_serializer.validated_data[
                    "trading_currency"
                ],
            },
        )
        if not alert_spread:
            return Response(
                {"error": "No spread alert found or created"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"alert_spread_created": alert_spread_created},
            status=(
                status.HTTP_201_CREATED if alert_spread_created else status.HTTP_200_OK
            ),
        )


class SingleMarketSpreadPoll(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_serializer = SingleMarketSpreadGetRequestSerializer(
            data=request.query_params
        )
        if not request_serializer.is_valid():
            return Response(
                request_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        current_market_spread, _ = calculate_single_market_spread(
            request_serializer.validated_data["market_id"]
        )
        if current_market_spread is None:
            return Response(
                {"error": "External Buda API not responding"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        market_alert_spread = MarketSpreadAlert.objects.filter(
            market_id=request_serializer.validated_data["market_id"]
        )
        if not market_alert_spread:
            return Response(
                {"error": "There is no alert_spread set for that market"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {
                "current_spread_above_alert": current_market_spread
                > market_alert_spread[0].alert_spread
            },
            status.HTTP_200_OK,
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
