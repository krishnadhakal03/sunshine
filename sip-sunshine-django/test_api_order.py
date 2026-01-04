
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip_sunshine.settings.development')
django.setup()

from django.test import Client
from restaurant.models import MenuItem, DeliverySettings, PaymentSettings
from decimal import Decimal
import json

client = Client()

# Create test data
item = MenuItem.objects.first()
if not item:
    item = MenuItem.objects.create(
        name='Test Pizza',
        price=Decimal('15.00'),
        category='Main'
    )

# Ensure settings exist
DeliverySettings.objects.get_or_create(defaults={'delivery_enabled': True})
PaymentSettings.objects.get_or_create(defaults={})

print(f"Using menu item: {item.name} (ID: {item.id}, Price: {item.price})")

# Test API order creation
order_data = {
    'order_type': 'seated',
    'guest_name': 'John Doe',
    'payment_method': 'cash',
    'table_number': 5,
    'special_requests': 'No onions',
    'items': [
        {
            'id': item.id,
            'name': item.name,
            'price': 15.00,
            'quantity': 2
        }
    ]
}

response = client.post(
    '/api/orders/create/',
    json.dumps(order_data),
    content_type='application/json'
)

print(f"API Response Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")
response_data = json.loads(response.content)
print(f"Response Success: {response_data.get('success')}")

if response_data.get('success'):
    print(f"Order created successfully!")
    print(f"Order ID: {response_data.get('order_id')}")
    print(f"Total: {response_data.get('total')}")
else:
    print(f"Order creation failed: {response_data.get('message')}")
