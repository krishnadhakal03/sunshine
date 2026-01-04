# Generated migration for adding address fields to Order model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_order_orderitem_order_restaurant__created_875601_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(blank=True, help_text='Street address for online orders', max_length=300, verbose_name='Delivery Address'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_city',
            field=models.CharField(blank=True, max_length=100, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_postal_code',
            field=models.CharField(blank=True, max_length=20, verbose_name='Postal Code'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_country',
            field=models.CharField(blank=True, max_length=100, verbose_name='Country'),
        ),
    ]
