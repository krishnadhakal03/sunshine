
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip_sunshine.settings.development')
django.setup()

from django.test import Client
from restaurant.models import MenuItem, DeliverySettings, PaymentSettings
from decimal import Decimal

# Create test data
client = Client()

# Create a test menu item
try:
    item = MenuItem.objects.create(
        name='Test Pizza',
        price=Decimal('15.00'),
        category='Main'
    )
    print(f"Created menu item: {item.id}")
except:
    item = MenuItem.objects.first()
    if item:
        print(f"Using existing menu item: {item.id}")

# Create settings if they don't exist
try:
    DeliverySettings.objects.get_or_create(defaults={'delivery_enabled': True})
    PaymentSettings.objects.get_or_create(defaults={'payment_enabled': True})
    print("Settings created/verified")
except Exception as e:
    print(f"Settings error: {e}")

# Test the API endpoint
import json
data = {
    'order_type': 'seated',
    'payment_method': 'cash',
    'guest_name': 'Test Guest',
    'guest_phone': '+1234567890',
    'table_number': 1,
    'items': [
        {'id': item.id, 'name': 'Test Pizza', 'price': 15.00, 'quantity': 1}
    ]
}

response = client.post(
    '/api/orders/create/',
    json.dumps(data),
    content_type='application/json'
)

print(f"Status Code: {response.status_code}")
print(f"Content Type: {response.get('Content-Type', 'Not set')}")
print(f"Response: {response.content.decode()[:500]}")
