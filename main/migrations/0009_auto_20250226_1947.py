# Generated by Django 3.2.25 on 2025-02-26 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_item_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB')], default='RUB', max_length=3, verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='order',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB')], default='RUB', max_length=3, verbose_name='Валюта'),
        ),
    ]
