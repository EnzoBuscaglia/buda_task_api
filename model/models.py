from django.db import models


class MarketSpreadAlert(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    market_id = models.CharField(max_length=50, unique=True)
    alert_spread = models.FloatField()
    trading_currency = models.CharField(max_length=50)

    def __str__(self):
        return f"Market {self.market_id} - Alert at {self.alert_spread} {self.trading_currency}"

    class Meta:
        ordering = ("market_id",)
