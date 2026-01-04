"""
Checkout and Order views for the restaurant app
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.utils import OperationalError, ProgrammingError
import logging
import re

from .models import Order, OrderItem, CustomerProfile

logger = logging.getLogger(__name__)


class CheckoutView(View):
    """
    Main checkout page - displays order summary and starts checkout flow
    """
    template_name = 'checkout/checkout.html'

    def get(self, request):
        context = {
            'page_title': 'Secure Checkout',
        }

        if request.user.is_authenticated:
            try:
                profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
                context['profile'] = profile
            except (OperationalError, ProgrammingError):
                context['profile'] = None
        return render(request, self.template_name, context)


class OrderConfirmationView(TemplateView):
    """
    Order confirmation page - shows after order is successfully created
    """
    template_name = 'checkout/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
            order_items = OrderItem.objects.filter(order=order)

            context['order'] = order
            context['order_items'] = order_items
            context['page_title'] = f'Order #{order.order_number} Confirmed'

            # Estimate completion time
            if order.estimated_completion_time:
                context['estimated_time'] = order.estimated_completion_time.strftime('%H:%M')
            else:
                context['estimated_time'] = 'Soon'

        except Order.DoesNotExist:
            context['error'] = 'Order not found'

        return context


class OrderTrackingView(TemplateView):
    """
    Order tracking page - allows customers to track their orders
    """
    template_name = 'checkout/tracking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Track Your Order'

        order_param = self.request.GET.get('order') or ''
        order_id_param = self.request.GET.get('order_id') or ''

        raw = (order_param or order_id_param).strip()
        context['order_query'] = raw

        if not raw:
            return context

        order_id = None
        if raw.isdigit():
            order_id = int(raw)
        else:
            match = re.match(r'^SIP-(\d+)$', raw, flags=re.IGNORECASE)
            if match:
                order_id = int(match.group(1))

        if not order_id:
            context['error'] = 'Invalid order reference'
            return context

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            context['error'] = 'Order not found'
            return context

        context['order'] = order
        context['order_items'] = OrderItem.objects.filter(order=order)
        if order.estimated_completion_time:
            context['estimated_time'] = order.estimated_completion_time.strftime('%H:%M')

        return context


class CreateOrderView(View):
    """
    Legacy view for creating orders (kept for compatibility)
    Redirects to checkout flow
    """
    def get(self, request):
        return redirect('restaurant:checkout')

    def post(self, request):
        return redirect('restaurant:checkout')
