# Generated by Django 4.2.7 on 2023-11-15 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Candle",
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
                ("datetime", models.DateTimeField()),
                ("open", models.FloatField()),
                ("high", models.FloatField()),
                ("low", models.FloatField()),
                ("close", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Sma",
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
                ("price", models.FloatField()),
                (
                    "candle",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="trade.candle"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ParabolicSAR",
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
                ("price", models.FloatField()),
                (
                    "candle",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="trade.candle"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MaxMin",
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
                ("price", models.FloatField()),
                (
                    "candle",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="trade.candle"
                    ),
                ),
            ],
        ),
    ]