from django.contrib import admin

from model.models import MarketSpreadAlert


class MarketSpreadAlertAdmin(admin.ModelAdmin):
    list_display = ("market_id", "alert_spread", "trading_currency")
    search_fields = ["market_id"]


admin.site.register(MarketSpreadAlert, MarketSpreadAlertAdmin)
