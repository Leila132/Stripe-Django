# Generated by Django 3.2.25 on 2025-02-26 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_order_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_price',
            new_name='price',
        ),
    ]
