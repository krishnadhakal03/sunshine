"""Customer journey smoke tests.

These are lightweight, browserless checks intended to validate the core
endpoints and templates for a happy-path ordering journey.

Note: The cart UI is stored in localStorage and driven by JavaScript, so we
validate server-rendered pages and backend APIs here.
"""

import json
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase

from restaurant.models import DeliverySettings, MenuItem, PaymentSettings


class JourneySmokeGuest(TestCase):
    def setUp(self):
        self.client = Client()
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()

        self.item = MenuItem.objects.create(
            name="Burger",
            description="Delicious burger",
            price=Decimal("12.50"),
            category="main_courses",
            is_active=True,
        )

    def test_guest_menu_checkout_tracking_chatbot(self):
        # Menu page
        response = self.client.get("/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger")

        # Checkout page loads and has expected modal ids
        response = self.client.get("/checkout/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "orderTypeModal")
        self.assertContains(response, "customerDetailsModal")
        self.assertContains(response, "orderReviewModal")

        # Create an order via API
        payload = {
            "order_type": "pickup",
            "payment_method": "cash",
            "guest_name": "Test Guest",
            "guest_phone": "+31612345678",
            "items": [
                {
                    "id": self.item.id,
                    "name": "Burger",
                    "price": 12.50,
                    "quantity": 1,
                }
            ],
        }
        response = self.client.post(
            "/api/orders/create/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("order_id", data)
        order_id = data["order_id"]

        # Order confirmation page
        response = self.client.get(f"/orders/confirmation/{order_id}/")
        self.assertEqual(response.status_code, 200)

        # Tracking page (supports query by id)
        response = self.client.get(f"/orders/tracking/?order_id={order_id}")
        self.assertEqual(response.status_code, 200)

        # Chatbot endpoint
        response = self.client.post(
            "/api/chatbot/",
            data=json.dumps({"message": "track my order"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        bot = response.json()
        self.assertIn("reply", bot)


class JourneySmokeLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()

        self.user = User.objects.create_user(
            username="journeyuser",
            email="journey@example.com",
            password="testpass123",
        )

        self.item = MenuItem.objects.create(
            name="Fries",
            description="Crispy",
            price=Decimal("5.00"),
            category="appetizers",
            is_active=True,
        )

    def test_logged_in_profile_and_tracking_page(self):
        logged_in = self.client.login(username="journeyuser", password="testpass123")
        self.assertTrue(logged_in)

        # Profile page should load for authenticated users
        response = self.client.get("/auth/profile/")
        self.assertEqual(response.status_code, 200)

        # Tracking page should load regardless of having an order
        response = self.client.get("/orders/tracking/")
        self.assertEqual(response.status_code, 200)

        # Create order and ensure status endpoint works
        payload = {
            "order_type": "seated",
            "payment_method": "cash",
            "guest_name": "Journey User",
            "guest_phone": "+31612345678",
            "table_number": 1,
            "items": [
                {
                    "id": self.item.id,
                    "name": "Fries",
                    "price": 5.00,
                    "quantity": 2,
                }
            ],
        }
        response = self.client.post(
            "/api/orders/create/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        order_id = response.json()["order_id"]

        response = self.client.get(f"/api/orders/{order_id}/")
        self.assertEqual(response.status_code, 200)
        status = response.json()
        self.assertIn("order_type", status)
        self.assertIn("status", status)
