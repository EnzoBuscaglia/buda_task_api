# Generated by Django 5.0.1 on 2024-01-29 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MarketSpreadAlert",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("market_id", models.CharField(max_length=50, unique=True)),
                ("alert_spread", models.FloatField()),
                ("trading_currency", models.CharField(max_length=50)),
            ],
            options={
                "ordering": ("market_id",),
            },
        ),
    ]