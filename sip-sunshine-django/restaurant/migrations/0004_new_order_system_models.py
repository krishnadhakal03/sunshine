# Generated migration for new order system models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0003_add_delivery_address_fields'),
    ]

    operations = [
        # Add new fields to Order model
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='preferred_pickup_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Preferred Pickup Time'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_instructions',
            field=models.TextField(blank=True, verbose_name='Delivery Instructions'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Delivery Charge'),
        ),
        migrations.AddField(
            model_name='order',
            name='estimated_delivery_time',
            field=models.IntegerField(blank=True, default=30, null=True, verbose_name='Est. Delivery Time (minutes)'),
        ),
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Subtotal'),
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Tax'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash on Delivery/Pickup'), ('stripe', 'Credit/Debit Card (Stripe)'), ('paypal', 'PayPal')], default='cash', max_length=20, verbose_name='Payment Method'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=20, verbose_name='Payment Status'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, help_text='Stripe or PayPal transaction ID', max_length=500, verbose_name='Payment ID'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_details',
            field=models.JSONField(blank=True, default=dict, help_text='Store payment metadata', verbose_name='Payment Details'),
        ),
        migrations.AddField(
            model_name='order',
            name='promised_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Promised Completion Time'),
        ),
        
        # Update order_type choices to include pickup
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('seated', 'Seated Customer'), ('pickup', 'Pickup Order'), ('delivery', 'Delivery Order')], default='seated', max_length=20, verbose_name='Order Type'),
        ),
        
        # Update status choices
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('preparing', 'Preparing'), ('ready', 'Ready'), ('out_for_delivery', 'Out for Delivery'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        
        # Create Cart model
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(help_text='Stored as JSON for flexibility', max_length=40, unique=True, verbose_name='Session Key')),
                ('items', models.JSONField(default=list, verbose_name='Cart Items')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Shopping Cart',
                'verbose_name_plural': 'Shopping Carts',
            },
        ),
        
        # Create DeliverySettings model
        migrations.CreateModel(
            name='DeliverySettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_enabled', models.BooleanField(default=True, verbose_name='Delivery Enabled')),
                ('pickup_enabled', models.BooleanField(default=True, verbose_name='Pickup Enabled')),
                ('delivery_charge_fixed', models.DecimalField(decimal_places=2, default='2.50', help_text='Fixed amount for all deliveries', max_digits=10, verbose_name='Fixed Delivery Charge')),
                ('delivery_charge_percent', models.DecimalField(decimal_places=2, default=0, help_text='Percentage of order total (leave 0 for fixed only)', max_digits=5, verbose_name='Delivery Charge %')),
                ('min_delivery_amount', models.DecimalField(decimal_places=2, default='10.00', help_text='Minimum order amount to qualify for delivery', max_digits=10, verbose_name='Minimum Delivery Amount')),
                ('min_pickup_amount', models.DecimalField(decimal_places=2, default='5.00', help_text='Minimum order amount for pickup orders', max_digits=10, verbose_name='Minimum Pickup Amount')),
                ('estimated_pickup_time', models.IntegerField(default=15, help_text='Default time to prepare pickup order', verbose_name='Est. Pickup Time (minutes)')),
                ('estimated_delivery_time', models.IntegerField(default=30, help_text='Average delivery time', verbose_name='Est. Delivery Time (minutes)')),
                ('max_delivery_radius', models.DecimalField(decimal_places=2, default='5', help_text='Maximum distance for delivery', max_digits=5, verbose_name='Max Delivery Radius (km)')),
                ('delivery_start_time', models.TimeField(default='11:00', verbose_name='Delivery Start Time')),
                ('delivery_end_time', models.TimeField(default='22:00', verbose_name='Delivery End Time')),
                ('pickup_start_time', models.TimeField(default='11:00', verbose_name='Pickup Start Time')),
                ('pickup_end_time', models.TimeField(default='22:00', verbose_name='Pickup End Time')),
            ],
            options={
                'verbose_name': 'Delivery Settings',
                'verbose_name_plural': 'Delivery Settings',
            },
        ),
        
        # Create PaymentSettings model
        migrations.CreateModel(
            name='PaymentSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gateway', models.CharField(choices=[('stripe', 'Stripe'), ('paypal', 'PayPal')], max_length=20, unique=True, verbose_name='Payment Gateway')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('is_test_mode', models.BooleanField(default=True, help_text='Use sandbox/test credentials', verbose_name='Test Mode')),
                ('stripe_public_key', models.CharField(blank=True, max_length=500, verbose_name='Stripe Public Key')),
                ('stripe_secret_key', models.CharField(blank=True, max_length=500, verbose_name='Stripe Secret Key')),
                ('paypal_client_id', models.CharField(blank=True, max_length=500, verbose_name='PayPal Client ID')),
                ('paypal_secret', models.CharField(blank=True, max_length=500, verbose_name='PayPal Secret')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Payment Settings',
                'verbose_name_plural': 'Payment Settings',
            },
        ),
        
        # Add database indexes
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['payment_status'], name='restaurant_o_payment_idx'),
        ),
    ]
