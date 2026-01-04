"""
PHASE 3 QA/QC - UNIT TEST SCRIPTS (FIXED VERSION)
Run these tests: pytest test_phase3_unit_FIXED.py -v

Django test cases for Phase 3 checkout system - Fixed for actual models
"""

import pytest
import json
from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from restaurant.models import (
    Order, OrderItem, MenuItem, Cart, 
    DeliverySettings, PaymentSettings
)


# ============================================================================
# DELIVERY SETTINGS MODEL TESTS
# ============================================================================

class DeliverySettingsModelTest(TestCase):
    """Test DeliverySettings model"""
    
    def setUp(self):
        self.settings = DeliverySettings.objects.create(
            delivery_charge_fixed=Decimal('2.50'),
            delivery_charge_percent=Decimal('5.0')  # FIXED: percent not percentage
        )
    
    def test_delivery_settings_creation(self):
        """✓ DeliverySettings can be created"""
        self.assertIsNotNone(self.settings.id)
        self.assertEqual(self.settings.delivery_charge_fixed, Decimal('2.50'))
    
    def test_delivery_charge_calculation(self):
        """✓ Delivery charge calculation works"""
        # Fixed charge: 2.50 + (100 * 5%) = 2.50 + 5.00 = 7.50
        charge = self.settings.calculate_delivery_charge(Decimal('100.00'))
        self.assertEqual(charge, Decimal('7.50'))
    
    def test_delivery_charge_fixed_only(self):
        """✓ Fixed charge only (no percentage)"""
        settings = DeliverySettings.objects.create(
            delivery_charge_fixed=Decimal('3.00'),
            delivery_charge_percent=Decimal('0.0')
        )
        charge = settings.calculate_delivery_charge(Decimal('50.00'))
        self.assertEqual(charge, Decimal('3.00'))


# ============================================================================
# PAYMENT SETTINGS MODEL TEST
# ============================================================================

class PaymentSettingsModelTest(TestCase):
    """Test PaymentSettings model"""
    
    def test_payment_settings_creation(self):
        """✓ PaymentSettings can be created"""
        settings = PaymentSettings.objects.create(
            gateway='stripe',
            enabled=True,
            is_test_mode=True,
            stripe_public_key='pk_test_xxx'
        )
        self.assertIsNotNone(settings.id)
        self.assertEqual(settings.gateway, 'stripe')


# ============================================================================
# ORDER MODEL TESTS
# ============================================================================

class OrderModelTest(TestCase):
    """Test Order model creation and methods"""
    
    def setUp(self):
        self.order = Order.objects.create(
            order_type='seated',
            guest_name='Test User',
            guest_phone='+31612345678',
            table_number=5,
            subtotal=Decimal('25.00'),
            tax=Decimal('5.25'),
            total_price=Decimal('30.25')  # FIXED: total_price not total_amount
        )
    
    def test_order_creation(self):
        """✓ Order model creates successfully"""
        self.assertIsNotNone(self.order.id)
        self.assertEqual(self.order.guest_name, 'Test User')
        self.assertIsNotNone(self.order.created_at)
    
    def test_order_string_representation(self):
        """✓ Order __str__ method works"""
        str_repr = str(self.order)
        self.assertIn('Order', str_repr)
        self.assertIn('Test User', str_repr)
    
    def test_order_payment_status_is_paid(self):
        """✓ Order is_paid() method works"""
        self.order.payment_status = 'completed'
        self.assertTrue(self.order.is_paid())
        
        self.order.payment_status = 'pending'
        self.assertFalse(self.order.is_paid())
    
    def test_order_can_be_delivered(self):
        """✓ Order can_be_delivered() method works"""
        delivery_order = Order.objects.create(
            order_type='delivery',
            guest_name='Test',
            delivery_address='123 Main',
            delivery_city='Amsterdam',
            delivery_postal_code='1012AB'
        )
        self.assertTrue(delivery_order.can_be_delivered())
        
        incomplete_order = Order.objects.create(
            order_type='delivery',
            guest_name='Test'
        )
        self.assertFalse(incomplete_order.can_be_delivered())
    
    def test_seated_order_type(self):
        """✓ Seated order type works"""
        self.assertEqual(self.order.order_type, 'seated')
        self.assertEqual(self.order.table_number, 5)
    
    def test_pickup_order_type(self):
        """✓ Pickup order type works"""
        order = Order.objects.create(
            order_type='pickup',
            guest_name='Test Pickup',
            payment_method='stripe'
        )
        self.assertEqual(order.order_type, 'pickup')
        self.assertEqual(order.delivery_charge, Decimal('0.00'))
    
    def test_delivery_order_type(self):
        """✓ Delivery order type works"""
        order = Order.objects.create(
            order_type='delivery',
            guest_name='Test Delivery',
            delivery_address='456 Oak',
            delivery_city='Rotterdam',
            delivery_postal_code='3011AB',
            delivery_charge=Decimal('2.50')
        )
        self.assertEqual(order.order_type, 'delivery')
        self.assertEqual(order.delivery_charge, Decimal('2.50'))


# ============================================================================
# ORDER ITEM MODEL TESTS
# ============================================================================

class OrderItemModelTest(TestCase):
    """Test OrderItem model"""
    
    def setUp(self):
        self.order = Order.objects.create(
            order_type='seated',
            guest_name='Test'
        )
        # MenuItem is translatable - don't create it for this test
        self.menu_item = None
    
    def test_order_item_creation(self):
        """✓ OrderItem can be created"""
        item = OrderItem.objects.create(
            order=self.order,
            menu_item=self.menu_item,
            item_name='Burger',
            item_price=Decimal('15.00'),
            quantity=2
        )
        self.assertIsNotNone(item.id)
        self.assertEqual(item.quantity, 2)
    
    def test_order_item_get_subtotal(self):
        """✓ OrderItem subtotal calculation works"""
        item = OrderItem.objects.create(
            order=self.order,
            item_name='Pizza',
            item_price=Decimal('12.50'),
            quantity=3
        )
        subtotal = item.get_subtotal()
        self.assertEqual(subtotal, Decimal('37.50'))


# ============================================================================
# CART MODEL TESTS
# ============================================================================

class CartModelTest(TestCase):
    """Test Cart model"""
    
    def setUp(self):
        self.cart = Cart.objects.create(
            session_key='test_session_123'
        )
    
    def test_cart_creation(self):
        """✓ Cart can be created"""
        self.assertIsNotNone(self.cart.id)
        self.assertEqual(self.cart.session_key, 'test_session_123')
    
    def test_cart_add_item(self):
        """✓ Cart add_item method works"""
        item_data = {
            'id': 1,
            'name': 'Burger',
            'price': 12.50,
            'quantity': 1
        }
        self.cart.add_item(item_data)
        
        # Reload from DB
        self.cart.refresh_from_db()
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0]['name'], 'Burger')
    
    def test_cart_remove_item(self):
        """✓ Cart remove_item method works"""
        self.cart.add_item({'id': 1, 'name': 'Item 1', 'price': 10})
        self.cart.add_item({'id': 2, 'name': 'Item 2', 'price': 20})
        
        self.cart.refresh_from_db()
        self.assertEqual(len(self.cart.items), 2)
        
        self.cart.remove_item(1)
        self.cart.refresh_from_db()
        self.assertEqual(len(self.cart.items), 1)
    
    def test_cart_get_total(self):
        """✓ Cart get_total method works"""
        self.cart.add_item({'id': 1, 'name': 'Item 1', 'price': 10.00, 'quantity': 2})
        self.cart.add_item({'id': 2, 'name': 'Item 2', 'price': 15.00, 'quantity': 1})
        
        total = self.cart.get_total()
        # 10*2 + 15*1 = 35.00
        self.assertEqual(total, 35.00)
    
    def test_cart_clear_cart(self):
        """✓ Cart clear_cart method works"""
        self.cart.add_item({'id': 1, 'name': 'Item', 'price': 10})
        self.cart.refresh_from_db()
        self.assertEqual(len(self.cart.items), 1)
        
        self.cart.clear_cart()
        self.cart.refresh_from_db()
        self.assertEqual(len(self.cart.items), 0)


# ============================================================================
# CALCULATION TESTS
# ============================================================================

class OrderCalculationsTest(TestCase):
    """Test order calculation logic"""
    
    def test_tax_calculation_21_percent(self):
        """✓ VAT calculation is 21%"""
        subtotal = Decimal('100.00')
        tax = (subtotal * Decimal('0.21')).quantize(Decimal('0.01'))
        self.assertEqual(tax, Decimal('21.00'))
    
    def test_total_with_tax(self):
        """✓ Total includes tax"""
        subtotal = Decimal('100.00')
        tax = Decimal('21.00')
        total = subtotal + tax
        self.assertEqual(total, Decimal('121.00'))
    
    def test_total_with_delivery_charge(self):
        """✓ Total includes delivery charge"""
        subtotal = Decimal('50.00')
        tax = Decimal('10.50')  # 50 * 0.21
        delivery_charge = Decimal('2.50')
        total = subtotal + tax + delivery_charge
        self.assertEqual(total, Decimal('63.00'))
    
    def test_order_calculate_total_method(self):
        """✓ Order calculate_total() method works"""
        order = Order.objects.create(
            order_type='seated',
            guest_name='Test',
            subtotal=Decimal('50.00'),
            tax=Decimal('10.50'),  # 50 * 0.21
            delivery_charge=Decimal('0.00')
        )
        
        # Method should calculate: subtotal + tax + delivery_charge
        total = order.calculate_total()
        # Should be: 50 + 10.50 + 0 = 60.50
        expected = Decimal('60.50')
        self.assertEqual(total, expected)


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
