# Generated migration for customer profile

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0004_new_order_system_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Phone')),
                ('delivery_address', models.CharField(blank=True, max_length=300, verbose_name='Delivery Address')),
                ('delivery_city', models.CharField(blank=True, max_length=100, verbose_name='City')),
                ('delivery_postal_code', models.CharField(blank=True, max_length=20, verbose_name='Postal Code')),
                ('delivery_country', models.CharField(blank=True, default='Netherlands', max_length=100, verbose_name='Country')),
                ('preferred_payment_method', models.CharField(choices=[('cash', 'Cash'), ('stripe', 'Credit/Debit Card (Stripe)'), ('paypal', 'PayPal')], default='cash', max_length=20, verbose_name='Preferred Payment Method')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Profile',
                'verbose_name_plural': 'Customer Profiles',
            },
        ),
    ]
