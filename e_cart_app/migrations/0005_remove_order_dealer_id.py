# Generated by Django 3.1.2 on 2020-11-09 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_cart_app', '0004_order_dealer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='dealer_id',
        ),
    ]