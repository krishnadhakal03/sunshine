"""Real UI journey tests (headless browser).

These tests use Playwright to validate the actual JavaScript-driven flow:
Menu → Add to Order → Cart modal → Checkout → Modals → Place Order → Confirmation.

Run:
  python manage.py test tests.test_ui_journey_playwright -v 2

Notes:
- The cart is stored in localStorage/sessionStorage, so a real browser is required.
- Playwright Chromium must be installed: `python -m playwright install chromium`
"""

import os
import re
from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate

from restaurant.models import DeliverySettings, MenuItem, PaymentSettings


# Playwright's sync API spins an event loop under the hood, which can trip
# Django's async-safety guard during test DB teardown. These are true E2E UI
# tests and do not rely on DB access after browser operations complete.
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')


class BasePlaywrightLiveServerTest(StaticLiveServerTestCase):
    _launch_args = [
        '--disable-gpu',
        '--disable-dev-shm-usage',
    ]

    @classmethod
    def _launch_browser(cls):
        cls._browser = cls._playwright.chromium.launch(
            headless=True,
            args=list(cls._launch_args),
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from playwright.sync_api import sync_playwright

        cls._playwright = sync_playwright().start()
        cls._launch_browser()

    @classmethod
    def tearDownClass(cls):
        try:
            cls._browser.close()
        finally:
            cls._playwright.stop()
            super().tearDownClass()

    def new_page(self):
        # If the browser process crashed/closed, relaunch once.
        try:
            if not self._browser.is_connected():
                type(self)._launch_browser()
        except Exception:
            type(self)._launch_browser()

        context = self._browser.new_context()
        page = context.new_page()
        page.set_default_timeout(20000)
        return context, page


class UIJourneyGuestPickup(BasePlaywrightLiveServerTest):
    def setUp(self):
        super().setUp()
        activate('en')
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()

        self.item = MenuItem.objects.create(
            price=Decimal("10.00"),
            category="appetizers",
            is_active=True,
        )
        for lang, name in (("en", "Playwright Burger"), ("nl", "Playwright Burger")):
            self.item.set_current_language(lang)
            self.item.name = name
            self.item.description = "E2E test item"
            self.item.save()

    def test_guest_pickup_place_order(self):
        context, page = self.new_page()
        try:
            url = f"{self.live_server_url}/menu/"
            try:
                response = page.goto(url)
            except Exception as e:
                # Common on some Windows setups: Chromium process closes on first use.
                if e.__class__.__name__ == 'TargetClosedError':
                    context.close()
                    context, page = self.new_page()
                    response = page.goto(url)
                else:
                    raise
            if response is None or response.status != 200:
                raise AssertionError(f"/menu/ did not return 200 (got {getattr(response, 'status', None)})")

            # Wait for server-rendered buttons to exist, then click.
            page.wait_for_selector(".menu-item-btn", state="attached")
            add_btn = page.locator(".menu-item-btn").first
            add_btn.scroll_into_view_if_needed()
            try:
                add_btn.click()
            except Exception:
                add_btn.click(force=True)

            # Cart modal should open
            page.wait_for_selector("#cartModal.show", state="visible")

            # Proceed to checkout via cart modal button
            page.locator("#cartModal button[onclick*='proceedToCheckout']").click()
            page.wait_for_url(re.compile(r".*/checkout/"))

            # Start checkout (opens order type modal)
            page.locator("button:has-text('Start Checkout')").click()
            page.wait_for_selector("#orderTypeModal.show", state="visible")

            # Choose Pickup
            page.locator("#orderTypeModal .order-type-card[onclick*='pickup']").click()

            # Customer details modal should open
            page.wait_for_selector("#customerDetailsModal.show", state="visible")
            page.fill("#guestName", "Playwright Guest")
            page.fill("#guestPhone", "+31612345678")

            # Continue to order review
            page.locator("#customerDetailsModal button[onclick*='proceedToDeliveryDetails']").click()

            # Order review modal should open
            page.wait_for_selector("#orderReviewModal.show", state="visible")

            # Agree to terms and place order
            page.check("#agreeTerms")
            page.locator("#orderReviewModal button[onclick*='submitOrder']").click()

            # Redirect to confirmation page
            page.wait_for_url(re.compile(r".*/orders/confirmation/\d+/$"))

            # Confirmation content
            page.wait_for_selector("text=Thank you for your order", state="visible")
        finally:
            context.close()


class UIJourneyLoggedInPickup(BasePlaywrightLiveServerTest):
    def setUp(self):
        super().setUp()
        activate('en')
        DeliverySettings.objects.create()
        PaymentSettings.objects.create()

        self.user_email = "playwright.user@example.com"
        self.user_password = "testpass123"
        User.objects.create_user(
            username="playwrightuser",
            email=self.user_email,
            password=self.user_password,
        )

        self.item = MenuItem.objects.create(
            price=Decimal("5.00"),
            category="appetizers",
            is_active=True,
        )
        for lang, name in (("en", "Playwright Fries"), ("nl", "Playwright Fries")):
            self.item.set_current_language(lang)
            self.item.name = name
            self.item.description = "E2E test item"
            self.item.save()

    def test_logged_in_pickup_place_order(self):
        context, page = self.new_page()
        try:
            # Login via UI
            page.goto(f"{self.live_server_url}/auth/login/")
            page.fill("#email", self.user_email)
            page.fill("#password", self.user_password)
            page.locator("button:has-text('Sign In')").click()

            # Profile should be accessible after login
            page.goto(f"{self.live_server_url}/auth/profile/")
            page.wait_for_selector("body")

            # Journey: menu → cart → checkout
            page.goto(f"{self.live_server_url}/menu/")
            page.wait_for_selector(".menu-item-btn", state="attached")
            add_btn = page.locator(".menu-item-btn").first
            add_btn.scroll_into_view_if_needed()
            try:
                add_btn.click()
            except Exception:
                add_btn.click(force=True)
            page.wait_for_selector("#cartModal.show", state="visible")
            page.locator("#cartModal button[onclick*='proceedToCheckout']").click()
            page.wait_for_url(re.compile(r".*/checkout/"))

            page.locator("button:has-text('Start Checkout')").click()
            page.wait_for_selector("#orderTypeModal.show", state="visible")
            page.locator("#orderTypeModal .order-type-card[onclick*='pickup']").click()

            page.wait_for_selector("#customerDetailsModal.show", state="visible")

            # For logged-in users, the modal may prefill; we still set if empty.
            if not page.locator("#guestName").input_value().strip():
                page.fill("#guestName", "Playwright User")
            if not page.locator("#guestPhone").input_value().strip():
                page.fill("#guestPhone", "+31612345678")

            page.locator("#customerDetailsModal button[onclick*='proceedToDeliveryDetails']").click()
            page.wait_for_selector("#orderReviewModal.show", state="visible")

            page.check("#agreeTerms")
            page.locator("#orderReviewModal button[onclick*='submitOrder']").click()
            page.wait_for_url(re.compile(r".*/orders/confirmation/\d+/$"))
            page.wait_for_selector("text=Thank you for your order", state="visible")
        finally:
            context.close()
