
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip_sunshine.settings.development')
django.setup()

from django.test import Client
from django.middleware.csrf import get_token
from restaurant.models import MenuItem
from decimal import Decimal

client = Client()

# Get CSRF token
response = client.get('/orders/create/')
print(f"GET /orders/create/ - Status: {response.status_code}")

# Create a test menu item
item = MenuItem.objects.first()
if item:
    print(f"Using menu item: {item.name} (ID: {item.id})")
else:
    item = MenuItem.objects.create(
        name='Test Burger',
        price=Decimal('12.50'),
        category='Main'
    )
    print(f"Created menu item: {item.name} (ID: {item.id})")

# Get CSRF token from the client
response = client.get('/')
csrf_token = response.cookies.get('csrftoken')
if not csrf_token:
    # Try to get it from a page with a form
    response = client.get('/menu/')
    csrf_token = response.cookies.get('csrftoken')

print(f"CSRF Token: {csrf_token}")

# Test POST to create order
data = {
    'guest_name': 'Test User',
    'item_name': 'Test Burger',
    'item_price': 12.50,
    'quantity': 1,
    'order_type': 'seated',
    'table_number': 5,
    'special_instructions': 'No onions'
}

response = client.post('/orders/create/', data)
print(f"POST /orders/create/ - Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type', 'Not set')}")
print(f"Response: {response.content.decode()[:500]}")
