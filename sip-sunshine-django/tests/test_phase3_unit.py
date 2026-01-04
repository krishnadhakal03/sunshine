"""
PHASE 3 QA/QC - UNIT TEST SCRIPTS
Run these tests: pytest test_phase3_unit.py -v

Django test cases for Phase 3 checkout system
"""

import pytest
import json
from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from restaurant.models import (
    Order, OrderItem, MenuItem, Cart, 
    DeliverySettings, PaymentSettings
)


# ============================================================================
# API ENDPOINT TESTS
# ============================================================================

class APIDeliverySettingsTest(TestCase):
    """Test GET /api/settings/delivery/ endpoint"""
    
    def setUp(self):
        self.client = Client()
        # Create delivery settings
        self.settings = DeliverySettings.objects.create(
            delivery_enabled=True,
            pickup_enabled=True,
            delivery_charge_fixed=Decimal('2.50'),
            delivery_charge_percentage=Decimal('0.0'),
            estimated_pickup_time=15,
            estimated_delivery_time=45,
            minimum_order_amount=Decimal('10.00'),
            service_radius_km=Decimal('10.0')
        )
    
    def test_delivery_settings_returns_200(self):
        """Test API returns 200 status"""
        response = self.client.get('/api/settings/delivery/')
        self.assertEqual(response.status_code, 200)
    
    def test_delivery_settings_returns_json(self):
        """Test API returns valid JSON"""
        response = self.client.get('/api/settings/delivery/')
        data = json.loads(response.content)
        self.assertIsInstance(data, dict)
    
    def test_delivery_settings_contains_required_fields(self):
        """Test response contains all required fields"""
        response = self.client.get('/api/settings/delivery/')
        data = json.loads(response.content)
        
        required_fields = [
            'delivery_enabled', 'pickup_enabled', 'delivery_charge_fixed',
            'delivery_charge_percentage', 'estimated_pickup_time',
            'estimated_delivery_time', 'minimum_order_amount', 'service_radius_km'
        ]
        for field in required_fields:
            self.assertIn(field, data)
    
    def test_delivery_settings_correct_values(self):
        """Test API returns correct values"""
        response = self.client.get('/api/settings/delivery/')
        data = json.loads(response.content)
        
        self.assertTrue(data['delivery_enabled'])
        self.assertTrue(data['pickup_enabled'])
        self.assertEqual(data['delivery_charge_fixed'], 2.50)
        self.assertEqual(data['estimated_pickup_time'], 15)
    
    def test_delivery_settings_no_record_returns_defaults(self):
        """Test API returns defaults when no settings exist"""
        DeliverySettings.objects.all().delete()
        response = self.client.get('/api/settings/delivery/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['delivery_enabled'])


class APICreateOrderTest(TestCase):
    """Test POST /api/orders/create/ endpoint"""
    
    def setUp(self):
        self.client = Client()
        self.url = '/api/orders/create/'
        
        # Create test menu item
        self.item = MenuItem.objects.create(
            name='Test Burger',
            description='Test Description',
            price=Decimal('12.50'),
            category='Main'
        )
        
        # Create settings
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()
    
    def test_create_valid_seated_order(self):
        """Test creating valid dine-in order"""
        data = {
            'order_type': 'seated',
            'payment_method': 'cash',
            'guest_name': 'Test User',
            'guest_phone': '+31612345678',
            'table_number': 5,
            'items': [
                {'id': self.item.id, 'name': 'Test Burger', 'price': 12.50, 'quantity': 2}
            ]
        }
        
        response = self.client.post(
            self.url,
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        self.assertIn('order_id', result)
        
        # Verify order created
        order = Order.objects.get(id=result['order_id'])
        self.assertEqual(order.order_type, 'seated')
        self.assertEqual(order.table_number, 5)
    
    def test_create_valid_pickup_order(self):
        """Test creating pickup order"""
        data = {
            'order_type': 'pickup',
            'payment_method': 'stripe',
            'guest_name': 'Jane Doe',
            'guest_phone': '+31687654321',
            'items': [{'id': self.item.id, 'name': 'Test Burger', 'price': 12.50, 'quantity': 1}]
        }
        
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        
        order = Order.objects.get(id=result['order_id'])
        self.assertEqual(order.order_type, 'pickup')
    
    def test_create_valid_delivery_order(self):
        """Test creating delivery order"""
        data = {
            'order_type': 'delivery',
            'payment_method': 'paypal',
            'guest_name': 'John Smith',
            'guest_phone': '+31611111111',
            'delivery_address': '123 Main St',
            'delivery_city': 'Amsterdam',
            'delivery_postal_code': '1012AB',
            'items': [{'id': self.item.id, 'name': 'Test Burger', 'price': 12.50, 'quantity': 1}]
        }
        
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        
        order = Order.objects.get(id=result['order_id'])
        self.assertEqual(order.delivery_address, '123 Main St')
        self.assertGreater(order.delivery_charge, 0)  # Should have charge
    
    def test_create_order_missing_required_field(self):
        """Test error handling for missing required fields"""
        data = {
            'payment_method': 'cash',
            'guest_name': 'Test',
            # Missing order_type
            'items': [{'name': 'Test', 'price': 10, 'quantity': 1}]
        }
        
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
    
    def test_create_order_invalid_order_type(self):
        """Test error handling for invalid order type"""
        data = {
            'order_type': 'invalid_type',
            'payment_method': 'cash',
            'guest_name': 'Test',
            'guest_phone': '+31612345678',
            'items': [{'name': 'Test', 'price': 10, 'quantity': 1}]
        }
        
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_order_totals_calculation(self):
        """Test order totals are calculated correctly"""
        data = {
            'order_type': 'seated',
            'payment_method': 'cash',
            'guest_name': 'Test',
            'guest_phone': '+31612345678',
            'table_number': 1,
            'items': [{'id': self.item.id, 'name': 'Test Burger', 'price': 10.00, 'quantity': 2}]
        }
        
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        result = json.loads(response.content)
        
        order = Order.objects.get(id=result['order_id'])
        
        # Verify calculations
        # Subtotal = 10 * 2 = 20
        self.assertEqual(order.subtotal, Decimal('20.00'))
        # Tax = 20 * 0.21 = 4.20
        self.assertEqual(order.tax, Decimal('4.20'))
        # Total = 20 + 4.20 = 24.20
        self.assertEqual(order.total_amount, Decimal('24.20'))


class APIGetOrderTest(TestCase):
    """Test GET /api/orders/{id}/ endpoint"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test order
        self.order = Order.objects.create(
            order_type='seated',
            status='pending',
            guest_name='Test User',
            guest_phone='+31612345678',
            payment_method='cash',
            subtotal=Decimal('20.00'),
            tax=Decimal('4.20'),
            total_amount=Decimal('24.20'),
            table_number=5
        )
    
    def test_get_order_valid_id(self):
        """Test retrieving order with valid ID"""
        response = self.client.get(f'/api/orders/{self.order.id}/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(data['id'], self.order.id)
        self.assertEqual(data['guest_name'], 'Test User')
        self.assertEqual(data['order_type'], 'seated')
    
    def test_get_order_invalid_id(self):
        """Test error handling for non-existent order"""
        response = self.client.get('/api/orders/99999/')
        
        self.assertEqual(response.status_code, 404)


# ============================================================================
# MODEL TESTS
# ============================================================================

class OrderModelTest(TestCase):
    """Test Order model"""
    
    def setUp(self):
        self.order = Order.objects.create(
            order_type='seated',
            status='pending',
            guest_name='Test',
            guest_phone='+31612345678',
            payment_method='cash',
            payment_status='unpaid',
            subtotal=Decimal('20.00'),
            tax=Decimal('4.20'),
            total_amount=Decimal('24.20')
        )
    
    def test_order_creation(self):
        """Test order is created correctly"""
        self.assertIsNotNone(self.order.id)
        self.assertIsNotNone(self.order.order_number)
    
    def test_order_string_representation(self):
        """Test order string representation"""
        self.assertIn(str(self.order.order_number), str(self.order))
    
    def test_order_payment_status_calculation(self):
        """Test payment status methods"""
        # Initially unpaid
        self.assertFalse(self.order.is_paid())
        
        # Update to paid
        self.order.payment_status = 'paid'
        self.order.save()
        self.assertTrue(self.order.is_paid())


class CartModelTest(TestCase):
    """Test Cart model"""
    
    def setUp(self):
        self.cart = Cart.objects.create(session_key='test_session')
    
    def test_cart_creation(self):
        """Test cart is created"""
        self.assertIsNotNone(self.cart.id)
    
    def test_cart_add_item(self):
        """Test adding item to cart"""
        self.cart.add_item({
            'id': 1,
            'name': 'Burger',
            'price': Decimal('12.50'),
            'quantity': 2
        })
        
        items = self.cart.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['quantity'], 2)
    
    def test_cart_get_total(self):
        """Test cart total calculation"""
        self.cart.add_item({'id': 1, 'name': 'Burger', 'price': Decimal('10.00'), 'quantity': 2})
        
        total = self.cart.get_total()
        # 10 * 2 * 1.21 = 24.20
        self.assertEqual(total, Decimal('24.20'))


class DeliverySettingsModelTest(TestCase):
    """Test DeliverySettings model"""
    
    def setUp(self):
        self.settings = DeliverySettings.objects.create(
            delivery_charge_fixed=Decimal('2.50'),
            delivery_charge_percentage=Decimal('5.0')
        )
    
    def test_delivery_charge_calculation(self):
        """Test delivery charge calculation"""
        charge = self.settings.calculate_delivery_charge(Decimal('100.00'))
        
        # Fixed 2.50 + 5% of 100 = 2.50 + 5.00 = 7.50
        expected = Decimal('2.50') + (Decimal('100.00') * Decimal('0.05'))
        self.assertEqual(charge, expected)


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
