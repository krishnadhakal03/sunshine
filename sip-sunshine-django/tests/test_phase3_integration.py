"""
PHASE 3 QA/QC - INTEGRATION & FLOW TEST SCRIPTS
Run these tests: pytest test_phase3_integration.py -v
"""

import json
import pytest
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse

from restaurant.models import (
    Order, OrderItem, MenuItem, DeliverySettings, PaymentSettings
)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class CartCheckoutIntegrationTest(TestCase):
    """Test Cart → Checkout integration"""
    
    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        
        # Create test menu items
        self.burger = MenuItem.objects.create(
            name='Burger',
            price=Decimal('12.50'),
            category='Main'
        )
        self.fries = MenuItem.objects.create(
            name='Fries',
            price=Decimal('5.00'),
            category='Side'
        )
        
        # Create settings
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()
    
    def test_checkout_page_loads(self):
        """Test checkout page loads successfully"""
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Secure Checkout')
    
    def test_checkout_page_includes_modals(self):
        """Test checkout page includes all modals"""
        response = self.client.get('/checkout/')
        
        self.assertContains(response, 'orderTypeModal')
        self.assertContains(response, 'customerDetailsModal')
        self.assertContains(response, 'orderReviewModal')


class APIOrderCreationIntegrationTest(TestCase):
    """Test API order creation integration"""
    
    def setUp(self):
        self.client = Client()
        self.url = '/api/orders/create/'
        
        # Create test item
        self.item = MenuItem.objects.create(
            name='Pizza',
            price=Decimal('15.00')
        )
        
        # Create settings
        self.delivery_settings = DeliverySettings.objects.create(
            delivery_charge_fixed=Decimal('2.50'),
            delivery_charge_percent=Decimal('0.0')
        )
        PaymentSettings.objects.create()
    
    def test_order_created_with_correct_items(self):
        """Test order created with correct items"""
        data = {
            'order_type': 'seated',
            'payment_method': 'cash',
            'guest_name': 'Test',
            'guest_phone': '+31612345678',
            'table_number': 1,
            'items': [
                {'id': self.item.id, 'name': 'Pizza', 'price': 15.00, 'quantity': 2}
            ]
        }
        
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        result = json.loads(response.content)
        
        # Verify order items created
        order_items = OrderItem.objects.filter(order_id=result['order_id'])
        self.assertEqual(order_items.count(), 1)
        self.assertEqual(order_items[0].quantity, 2)
        self.assertEqual(order_items[0].item_name, 'Pizza')
    
    def test_delivery_order_includes_delivery_charge(self):
        """Test delivery order includes delivery charge"""
        data = {
            'order_type': 'delivery',
            'payment_method': 'cash',
            'guest_name': 'Test',
            'guest_phone': '+31612345678',
            'delivery_address': '123 Main',
            'delivery_city': 'Amsterdam',
            'delivery_postal_code': '1012AB',
            'items': [{'id': self.item.id, 'name': 'Pizza', 'price': 15.00, 'quantity': 1}]
        }
        
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        result = json.loads(response.content)
        
        order = Order.objects.get(id=result['order_id'])
        self.assertEqual(order.delivery_charge, Decimal('2.50'))
        
        # Total should include delivery charge
        expected_total = Decimal('15.00') + (Decimal('15.00') * Decimal('0.21')) + Decimal('2.50')
        self.assertEqual(order.total_price, expected_total)
    
    def test_seated_order_no_delivery_charge(self):
        """Test seated order has no delivery charge"""
        data = {
            'order_type': 'seated',
            'payment_method': 'cash',
            'guest_name': 'Test',
            'guest_phone': '+31612345678',
            'table_number': 1,
            'items': [{'id': self.item.id, 'name': 'Pizza', 'price': 15.00, 'quantity': 1}]
        }
        
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        result = json.loads(response.content)
        
        order = Order.objects.get(id=result['order_id'])
        self.assertEqual(order.delivery_charge, Decimal('0.00'))


class AdminIntegrationTest(TestCase):
    """Test Django admin integration"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test order
        self.order = Order.objects.create(
            order_type='seated',
            guest_name='Test',
            guest_phone='+31612345678',
            table_number=1
        )
    
    def test_order_visible_in_admin(self):
        """Test order appears in admin list"""
        # Note: This would require admin authentication
        # For now, just verify order can be retrieved
        retrieved_order = Order.objects.get(id=self.order.id)
        self.assertEqual(retrieved_order.guest_name, 'Test')


# ============================================================================
# FLOW TESTS
# ============================================================================

class SeatedDineInFlowTest(TestCase):
    """Test complete seated dine-in order flow"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test items
        self.burger = MenuItem.objects.create(
            name='Burger',
            price=Decimal('12.50')
        )
        self.fries = MenuItem.objects.create(
            name='Fries',
            price=Decimal('5.00')
        )
        
        # Create settings
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()
    
    def test_complete_seated_flow(self):
        """Test complete seated order flow"""
        # Step 1: Create order via API
        order_data = {
            'order_type': 'seated',
            'payment_method': 'cash',
            'guest_name': 'John Doe',
            'guest_phone': '+31612345678',
            'guest_email': 'john@example.com',
            'table_number': 5,
            'special_requests': 'Extra sauce',
            'items': [
                {'id': self.burger.id, 'name': 'Burger', 'price': 12.50, 'quantity': 2},
                {'id': self.fries.id, 'name': 'Fries', 'price': 5.00, 'quantity': 1}
            ]
        }
        
        response = self.client.post(
            '/api/orders/create/',
            json.dumps(order_data),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        order_id = result['order_id']
        
        # Step 2: Verify order in database
        order = Order.objects.get(id=order_id)
        self.assertEqual(order.order_type, 'seated')
        self.assertEqual(order.guest_name, 'John Doe')
        self.assertEqual(order.table_number, 5)
        self.assertEqual(order.payment_method, 'cash')
        self.assertEqual(order.special_requests, 'Extra sauce')
        
        # Step 3: Verify items
        items = OrderItem.objects.filter(order=order)
        self.assertEqual(items.count(), 2)
        
        # Step 4: Verify totals
        # Burger: 12.50 * 2 = 25.00
        # Fries: 5.00 * 1 = 5.00
        # Subtotal: 30.00
        # Tax (21%): 6.30
        # Total: 36.30
        self.assertEqual(order.subtotal, Decimal('30.00'))
        self.assertEqual(order.tax, Decimal('6.30'))
        self.assertEqual(order.total_price, Decimal('36.30'))
        self.assertEqual(order.delivery_charge, Decimal('0.00'))
        
        # Step 5: Verify order status
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.payment_status, 'unpaid')


class PickupOrderFlowTest(TestCase):
    """Test complete pickup order flow"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test item
        self.item = MenuItem.objects.create(
            name='Pizza',
            price=Decimal('15.00')
        )
        
        # Create settings
        DeliverySettings.objects.create(
            estimated_pickup_time=15
        )
        PaymentSettings.objects.create()
    
    def test_complete_pickup_flow(self):
        """Test complete pickup order flow"""
        order_data = {
            'order_type': 'pickup',
            'payment_method': 'stripe',
            'guest_name': 'Jane Smith',
            'guest_phone': '+31687654321',
            'preferred_pickup_time': '2024-01-15T14:30',
            'items': [
                {'id': self.item.id, 'name': 'Pizza', 'price': 15.00, 'quantity': 2}
            ]
        }
        
        response = self.client.post(
            '/api/orders/create/',
            json.dumps(order_data),
            content_type='application/json'
        )
        
        result = json.loads(response.content)
        order = Order.objects.get(id=result['order_id'])
        
        # Verify
        self.assertEqual(order.order_type, 'pickup')
        self.assertEqual(order.payment_method, 'stripe')
        self.assertIsNotNone(order.preferred_pickup_time)
        self.assertEqual(order.delivery_charge, Decimal('0.00'))
        
        # Verify totals: 15 * 2 = 30, tax = 6.30, total = 36.30
        self.assertEqual(order.total_price, Decimal('36.30'))


class DeliveryOrderFlowTest(TestCase):
    """Test complete delivery order flow"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test item
        self.item = MenuItem.objects.create(
            name='Burger',
            price=Decimal('12.50')
        )
        
        # Create settings
        DeliverySettings.objects.create(
            delivery_charge_fixed=Decimal('2.50'),
            delivery_charge_percent=Decimal('0.0')
        )
        PaymentSettings.objects.create()
    
    def test_complete_delivery_flow(self):
        """Test complete delivery order flow"""
        order_data = {
            'order_type': 'delivery',
            'payment_method': 'paypal',
            'guest_name': 'Bob Johnson',
            'guest_phone': '+31611111111',
            'delivery_address': '456 Oak Avenue',
            'delivery_city': 'Rotterdam',
            'delivery_postal_code': '3011AB',
            'delivery_instructions': 'Leave at door',
            'items': [
                {'id': self.item.id, 'name': 'Burger', 'price': 12.50, 'quantity': 1}
            ]
        }
        
        response = self.client.post(
            '/api/orders/create/',
            json.dumps(order_data),
            content_type='application/json'
        )
        
        result = json.loads(response.content)
        order = Order.objects.get(id=result['order_id'])
        
        # Verify delivery details
        self.assertEqual(order.order_type, 'delivery')
        self.assertEqual(order.delivery_address, '456 Oak Avenue')
        self.assertEqual(order.delivery_city, 'Rotterdam')
        self.assertEqual(order.delivery_postal_code, '3011AB')
        self.assertEqual(order.delivery_instructions, 'Leave at door')
        
        # Verify charge included
        self.assertEqual(order.delivery_charge, Decimal('2.50'))
        
        # Verify totals: 12.50 + tax (2.625 → 2.62) + charge (2.50) = 17.62
        tax = (Decimal('12.50') * Decimal('0.21')).quantize(Decimal('0.01'))
        expected_total = Decimal('12.50') + tax + Decimal('2.50')
        self.assertEqual(order.total_price, expected_total)


class MultiItemOrderFlowTest(TestCase):
    """Test order with multiple different items"""
    
    def setUp(self):
        self.client = Client()
        
        # Create multiple items
        self.items = [
            MenuItem.objects.create(name=f'Item {i}', price=Decimal(f'{10 + i}.00'))
            for i in range(5)
        ]
        
        # Create settings
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()
    
    def test_multi_item_order(self):
        """Test order with 5 different items"""
        items_data = [
            {'id': self.items[i].id, 'name': f'Item {i}', 'price': float(10 + i), 'quantity': i + 1}
            for i in range(5)
        ]
        
        order_data = {
            'order_type': 'seated',
            'payment_method': 'cash',
            'guest_name': 'Multi Item Customer',
            'guest_phone': '+31612345678',
            'table_number': 1,
            'items': items_data
        }
        
        response = self.client.post(
            '/api/orders/create/',
            json.dumps(order_data),
            content_type='application/json'
        )
        
        result = json.loads(response.content)
        order = Order.objects.get(id=result['order_id'])
        
        # Verify all items created
        order_items = OrderItem.objects.filter(order=order)
        self.assertEqual(order_items.count(), 5)
        
        # Verify quantities
        for i, item in enumerate(order_items):
            self.assertEqual(item.quantity, i + 1)


class ValidationFlowTest(TestCase):
    """Test validation errors in checkout flow"""
    
    def setUp(self):
        self.client = Client()
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()
    
    def test_missing_required_field_seated(self):
        """Test error when table_number missing for seated order"""
        order_data = {
            'order_type': 'seated',
            'payment_method': 'cash',
            'guest_name': 'Test',
            'guest_phone': '+31612345678',
            # Missing table_number
            'items': [{'name': 'Item', 'price': 10, 'quantity': 1}]
        }
        
        response = self.client.post(
            '/api/orders/create/',
            json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
    
    def test_missing_address_delivery(self):
        """Test error when address missing for delivery order"""
        order_data = {
            'order_type': 'delivery',
            'payment_method': 'cash',
            'guest_name': 'Test',
            'guest_phone': '+31612345678',
            # Missing delivery_address
            'delivery_city': 'Amsterdam',
            'delivery_postal_code': '1012AB',
            'items': [{'name': 'Item', 'price': 10, 'quantity': 1}]
        }
        
        response = self.client.post(
            '/api/orders/create/',
            json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_empty_items_array(self):
        """Test error when items array is empty"""
        order_data = {
            'order_type': 'seated',
            'payment_method': 'cash',
            'guest_name': 'Test',
            'guest_phone': '+31612345678',
            'table_number': 1,
            'items': []  # Empty items
        }
        
        response = self.client.post(
            '/api/orders/create/',
            json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
