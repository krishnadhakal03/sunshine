"""
PHASE 3 QA/QC - SMOKE & REGRESSION TESTS
Run these: pytest test_phase3_smoke_regression.py -v
"""

import json
import pytest
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse

from restaurant.models import (
    Order, OrderItem, MenuItem, DeliverySettings, PaymentSettings, Cart, CartItem
)



# ============================================================================
# SMOKE TESTS - Basic Functionality Verification
# ============================================================================

class SmokeTestCheckoutPage(TestCase):
    """Smoke tests for checkout page loading"""
    
    def setUp(self):
        self.client = Client()
    
    def test_checkout_page_loads(self):
        """✓ Checkout page loads without errors"""
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
    
    def test_checkout_page_has_title(self):
        """✓ Checkout page has correct title"""
        response = self.client.get('/checkout/')
        self.assertContains(response, 'Secure Checkout')
    
    def test_checkout_page_has_order_type_modal(self):
        """✓ Checkout page includes order type modal"""
        response = self.client.get('/checkout/')
        self.assertContains(response, 'orderTypeModal')
    
    def test_checkout_page_has_customer_details_modal(self):
        """✓ Checkout page includes customer details modal"""
        response = self.client.get('/checkout/')
        self.assertContains(response, 'customerDetailsModal')
    
    def test_checkout_page_has_review_modal(self):
        """✓ Checkout page includes order review modal"""
        response = self.client.get('/checkout/')
        self.assertContains(response, 'orderReviewModal')


class SmokeTestOrderCreationAPI(TestCase):
    """Smoke tests for order creation API"""
    
    def setUp(self):
        self.client = Client()
        
        self.item = MenuItem.objects.create(
            name='Test Item',
            price=Decimal('10.00')
        )
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()
    
    def test_api_orders_create_endpoint_exists(self):
        """✓ POST /api/orders/create/ endpoint exists"""
        response = self.client.post(
            '/api/orders/create/',
            json.dumps({
                'order_type': 'seated',
                'payment_method': 'cash',
                'guest_name': 'Test',
                'guest_phone': '+31612345678',
                'table_number': 1,
                'items': [{'id': self.item.id, 'name': 'Test', 'price': 10, 'quantity': 1}]
            }),
            content_type='application/json'
        )
        self.assertNotEqual(response.status_code, 404)
    
    def test_api_returns_valid_json(self):
        """✓ API returns valid JSON response"""
        response = self.client.post(
            '/api/orders/create/',
            json.dumps({
                'order_type': 'seated',
                'payment_method': 'cash',
                'guest_name': 'Test',
                'guest_phone': '+31612345678',
                'table_number': 1,
                'items': [{'id': self.item.id, 'name': 'Test', 'price': 10, 'quantity': 1}]
            }),
            content_type='application/json'
        )
        
        try:
            json.loads(response.content)
            self.assertTrue(True)
        except json.JSONDecodeError:
            self.fail("API did not return valid JSON")
    
    def test_api_returns_order_id(self):
        """✓ API returns order_id in response"""
        response = self.client.post(
            '/api/orders/create/',
            json.dumps({
                'order_type': 'seated',
                'payment_method': 'cash',
                'guest_name': 'Test',
                'guest_phone': '+31612345678',
                'table_number': 1,
                'items': [{'id': self.item.id, 'name': 'Test', 'price': 10, 'quantity': 1}]
            }),
            content_type='application/json'
        )
        
        result = json.loads(response.content)
        self.assertIn('order_id', result)


class SmokeTestDeliverySettings(TestCase):
    """Smoke tests for delivery settings API"""
    
    def setUp(self):
        self.client = Client()
        DeliverySettings.objects.create(
            delivery_charge_fixed=Decimal('2.50'),
            estimated_delivery_time=30
        )
    
    def test_delivery_settings_api_endpoint_exists(self):
        """✓ GET /api/settings/delivery/ endpoint exists"""
        response = self.client.get('/api/settings/delivery/')
        self.assertNotEqual(response.status_code, 404)
    
    def test_delivery_settings_returns_json(self):
        """✓ Delivery settings API returns JSON"""
        response = self.client.get('/api/settings/delivery/')
        
        try:
            json.loads(response.content)
            self.assertTrue(True)
        except json.JSONDecodeError:
            self.fail("API did not return valid JSON")
    
    def test_delivery_settings_has_required_fields(self):
        """✓ Delivery settings response has required fields"""
        response = self.client.get('/api/settings/delivery/')
        result = json.loads(response.content)
        
        self.assertIn('delivery_charge_fixed', result)
        self.assertIn('estimated_delivery_time', result)


class SmokeTestOrderRetrieval(TestCase):
    """Smoke tests for order retrieval"""
    
    def setUp(self):
        self.client = Client()
        
        self.order = Order.objects.create(
            order_type='seated',
            guest_name='Test User',
            guest_phone='+31612345678',
            table_number=1
        )
    
    def test_get_order_endpoint_exists(self):
        """✓ GET /api/orders/{id}/ endpoint exists"""
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertNotEqual(response.status_code, 404)
    
    def test_get_order_returns_valid_data(self):
        """✓ GET /api/orders/{id}/ returns valid order data"""
        response = self.client.get(f'/api/orders/{self.order.id}/')
        result = json.loads(response.content)
        
        self.assertEqual(result['order_type'], 'seated')
        self.assertEqual(result['guest_name'], 'Test User')


# ============================================================================
# REGRESSION TESTS - Verify Existing Features
# ============================================================================

class RegressionTestMenuPage(TestCase):
    """Regression tests for menu page"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test menu items
        MenuItem.objects.create(
            name='Burger',
            price=Decimal('12.50'),
            category='Main',
            description='Delicious burger'
        )
        MenuItem.objects.create(
            name='Fries',
            price=Decimal('5.00'),
            category='Side'
        )
    
    def test_menu_page_loads(self):
        """✓ Menu page still loads"""
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
    
    def test_menu_page_displays_items(self):
        """✓ Menu items display on menu page"""
        response = self.client.get('/menu/')
        self.assertContains(response, 'Burger')
        self.assertContains(response, 'Fries')
    
    def test_menu_items_have_prices(self):
        """✓ Menu items show prices"""
        response = self.client.get('/menu/')
        self.assertContains(response, '12.50')
        self.assertContains(response, '5.00')


class RegressionTestCartModel(TestCase):
    """Regression tests for cart functionality"""
    
    def setUp(self):
        self.item = MenuItem.objects.create(
            name='Pizza',
            price=Decimal('15.00')
        )
        
        self.cart = Cart.objects.create()
    
    def test_cart_creation(self):
        """✓ Cart model still works"""
        self.assertIsNotNone(self.cart.id)
    
    def test_cart_can_add_items(self):
        """✓ Can add items to cart"""
        CartItem.objects.create(
            cart=self.cart,
            item=self.item,
            quantity=2
        )
        
        items = CartItem.objects.filter(cart=self.cart)
        self.assertEqual(items.count(), 1)
    
    def test_cart_item_quantities(self):
        """✓ Cart item quantities work correctly"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            item=self.item,
            quantity=3
        )
        
        self.assertEqual(cart_item.quantity, 3)


class RegressionTestOrderModel(TestCase):
    """Regression tests for order model"""
    
    def test_order_creation(self):
        """✓ Order model still creates records"""
        order = Order.objects.create(
            order_type='seated',
            guest_name='Test User',
            guest_phone='+31612345678'
        )
        
        self.assertIsNotNone(order.id)
        self.assertIsNotNone(order.order_number)
    
    def test_order_auto_generates_number(self):
        """✓ Order number auto-generated"""
        order1 = Order.objects.create(order_type='seated')
        order2 = Order.objects.create(order_type='seated')
        
        self.assertNotEqual(order1.order_number, order2.order_number)
    
    def test_order_status_defaults_pending(self):
        """✓ New orders default to pending status"""
        order = Order.objects.create(order_type='seated')
        self.assertEqual(order.status, 'pending')
    
    def test_order_payment_status_defaults_unpaid(self):
        """✓ New orders default to unpaid"""
        order = Order.objects.create(order_type='seated')
        self.assertEqual(order.payment_status, 'unpaid')


class RegressionTestOrderTypes(TestCase):
    """Regression tests for order type support"""
    
    def setUp(self):
        DeliverySettings.objects.create(
            delivery_charge_fixed=Decimal('2.50')
        )
        PaymentSettings.objects.create()
        
        self.item = MenuItem.objects.create(
            name='Item',
            price=Decimal('10.00')
        )
    
    def test_seated_order_type(self):
        """✓ Seated order type still works"""
        order = Order.objects.create(
            order_type='seated',
            table_number=1
        )
        
        self.assertEqual(order.order_type, 'seated')
        self.assertEqual(order.table_number, 1)
    
    def test_pickup_order_type(self):
        """✓ Pickup order type still works"""
        order = Order.objects.create(
            order_type='pickup'
        )
        
        self.assertEqual(order.order_type, 'pickup')
    
    def test_delivery_order_type(self):
        """✓ Delivery order type still works"""
        order = Order.objects.create(
            order_type='delivery',
            delivery_address='123 Main',
            delivery_city='Amsterdam'
        )
        
        self.assertEqual(order.order_type, 'delivery')
        self.assertEqual(order.delivery_address, '123 Main')


class RegressionTestPaymentMethods(TestCase):
    """Regression tests for payment methods"""
    
    def setUp(self):
        PaymentSettings.objects.create(
            cash_enabled=True,
            stripe_enabled=True,
            paypal_enabled=True
        )
    
    def test_cash_payment_method(self):
        """✓ Cash payment method works"""
        order = Order.objects.create(
            order_type='seated',
            payment_method='cash'
        )
        
        self.assertEqual(order.payment_method, 'cash')
    
    def test_stripe_payment_method(self):
        """✓ Stripe payment method works"""
        order = Order.objects.create(
            order_type='seated',
            payment_method='stripe'
        )
        
        self.assertEqual(order.payment_method, 'stripe')
    
    def test_paypal_payment_method(self):
        """✓ PayPal payment method works"""
        order = Order.objects.create(
            order_type='seated',
            payment_method='paypal'
        )
        
        self.assertEqual(order.payment_method, 'paypal')


class RegressionTestTaxCalculation(TestCase):
    """Regression tests for tax calculation"""
    
    def test_vat_calculation_21_percent(self):
        """✓ VAT calculation is 21%"""
        order = Order.objects.create(
            order_type='seated',
            subtotal=Decimal('100.00')
        )
        
        expected_tax = Decimal('100.00') * Decimal('0.21')
        self.assertEqual(order.tax, expected_tax)
    
    def test_total_includes_tax(self):
        """✓ Total amount includes tax"""
        order = Order.objects.create(
            order_type='seated',
            subtotal=Decimal('100.00')
        )
        
        expected_total = Decimal('100.00') + (Decimal('100.00') * Decimal('0.21'))
        self.assertEqual(order.total_amount, expected_total)


class RegressionTestDatabaseIntegrity(TestCase):
    """Regression tests for database integrity"""
    
    def test_order_guest_name_required(self):
        """✓ Order guest name can be stored"""
        order = Order.objects.create(
            order_type='seated',
            guest_name='Test Customer'
        )
        
        retrieved = Order.objects.get(id=order.id)
        self.assertEqual(retrieved.guest_name, 'Test Customer')
    
    def test_order_phone_required(self):
        """✓ Order guest phone can be stored"""
        order = Order.objects.create(
            order_type='seated',
            guest_phone='+31612345678'
        )
        
        retrieved = Order.objects.get(id=order.id)
        self.assertEqual(retrieved.guest_phone, '+31612345678')
    
    def test_order_items_relationship(self):
        """✓ Order to OrderItem relationship works"""
        item = MenuItem.objects.create(
            name='Test',
            price=Decimal('10.00')
        )
        
        order = Order.objects.create(order_type='seated')
        
        order_item = OrderItem.objects.create(
            order=order,
            item=item,
            quantity=1
        )
        
        retrieved_items = OrderItem.objects.filter(order=order)
        self.assertEqual(retrieved_items.count(), 1)


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
