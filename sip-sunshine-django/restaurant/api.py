"""
Restaurant API endpoints for cart, checkout, and orders
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from decimal import Decimal
import logging

from .chatbot import generate_reply

from .models import (
    Order, OrderItem, Cart, MenuItem,
    DeliverySettings, PaymentSettings
)

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
@csrf_exempt
def chatbot_message(request):
    """POST /api/chatbot/

    Minimal local chatbot (no paid APIs). Request body:
    {"message": "..."}
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    message = (data.get('message') or '').strip()
    if not message:
        return JsonResponse({'success': False, 'message': 'Message is required'}, status=400)
    if len(message) > 500:
        return JsonResponse({'success': False, 'message': 'Message too long'}, status=400)

    reply, intent, confidence = generate_reply(message)

    # Small enhancement: if user is logged in, remind them where “my order” lives.
    if intent == 'tracking' and getattr(request, 'user', None) and request.user.is_authenticated:
        reply = reply + "\n\nTip: You can also check your current order in Profile." 

    return JsonResponse({
        'success': True,
        'reply': reply,
        'intent': intent,
        'confidence': confidence,
    })


@require_http_methods(["GET"])
def get_delivery_settings(request):
    """
    GET /api/settings/delivery/
    Returns delivery settings (charges, times, etc.)
    """
    try:
        settings = DeliverySettings.objects.first()
        if not settings:
            # Return defaults if no settings exist
            return JsonResponse({
                'delivery_enabled': True,
                'pickup_enabled': True,
                'delivery_charge_fixed': 2.50,
                'delivery_charge_percent': 0.0,
                'estimated_pickup_time': 15,
                'estimated_delivery_time': 30,
                'min_delivery_amount': 10.00,
                'min_pickup_amount': 5.00
            })

        return JsonResponse({
            'delivery_enabled': settings.delivery_enabled,
            'pickup_enabled': settings.pickup_enabled,
            'delivery_charge_fixed': float(settings.delivery_charge_fixed),
            'delivery_charge_percent': float(settings.delivery_charge_percent),
            # Legacy aliases used by Phase 3 unit tests
            'delivery_charge_percentage': float(settings.delivery_charge_percent),
            'estimated_pickup_time': settings.estimated_pickup_time,
            'estimated_delivery_time': settings.estimated_delivery_time,
            'min_delivery_amount': float(settings.min_delivery_amount),
            'min_pickup_amount': float(settings.min_pickup_amount),
            # Legacy aliases used by Phase 3 unit tests
            'minimum_order_amount': float(settings.min_delivery_amount),
            'service_radius_km': float(getattr(settings, 'max_delivery_radius', 0) or 0),
        })
    except Exception as e:
        logger.error(f"Error fetching delivery settings: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def create_order(request):
    """
    POST /api/orders/create/
    Creates a new order from checkout data
    
    Request body:
    {
        "order_type": "seated|pickup|delivery",
        "payment_method": "cash|stripe|paypal",
        "guest_name": "John Doe",
        "guest_email": "john@example.com",
        "guest_phone": "+31612345678",
        "table_number": 5,  # for seated orders
        "preferred_pickup_time": "2024-01-15T14:30",  # for pickup orders
        "delivery_address": "123 Main St",  # for delivery orders
        "delivery_city": "Amsterdam",
        "delivery_postal_code": "1012AB",
        "delivery_instructions": "Ring doorbell twice",
        "special_requests": "No onions please",
        "items": [
            {"id": 1, "name": "Burger", "price": 12.50, "quantity": 2, "special_instructions": ""}
        ]
    }
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    try:
        with transaction.atomic():
            # Validate required fields
            required_fields = ['order_type', 'payment_method', 'guest_name', 'guest_phone', 'items']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'success': False,
                        'message': f'Missing required field: {field}'
                    }, status=400)

            # Validate order type
            valid_order_types = ['seated', 'pickup', 'delivery']
            if data['order_type'] not in valid_order_types:
                return JsonResponse({
                    'success': False,
                    'message': f'Invalid order type. Must be one of: {", ".join(valid_order_types)}'
                }, status=400)

            # Validate payment method
            valid_payment_methods = ['cash', 'stripe', 'paypal']
            if data['payment_method'] not in valid_payment_methods:
                return JsonResponse({
                    'success': False,
                    'message': f'Invalid payment method. Must be one of: {", ".join(valid_payment_methods)}'
                }, status=400)

            # Validate order-type specific requirements
            if data['order_type'] == 'seated' and not data.get('table_number'):
                return JsonResponse({
                    'success': False,
                    'message': 'Table number required for dine-in orders'
                }, status=400)

            if data['order_type'] == 'delivery':
                required_delivery_fields = ['delivery_address', 'delivery_city', 'delivery_postal_code']
                for field in required_delivery_fields:
                    if not data.get(field):
                        return JsonResponse({
                            'success': False,
                            'message': f'Missing delivery field: {field}'
                        }, status=400)

            # Validate items
            if not data.get('items') or len(data['items']) == 0:
                return JsonResponse({
                    'success': False,
                    'message': 'Order must contain at least one item'
                }, status=400)

            # Calculate totals
            subtotal = Decimal('0.00')
            for item in data['items']:
                if not item.get('price') or not item.get('quantity'):
                    return JsonResponse({
                        'success': False,
                        'message': f'Invalid item data'
                    }, status=400)
                subtotal += Decimal(str(item['price'])) * item['quantity']

            # Calculate tax (21% for Netherlands)
            tax = (subtotal * Decimal('0.21')).quantize(Decimal('0.01'))

            # Calculate delivery charge if applicable
            delivery_charge = Decimal('0.00')
            if data['order_type'] == 'delivery':
                try:
                    settings = DeliverySettings.objects.first()
                    if settings:
                        # Fixed charge + percentage
                        fixed_charge = Decimal(str(settings.delivery_charge_fixed))
                        percentage_charge = (subtotal * Decimal(str(settings.delivery_charge_percent)) / 100).quantize(Decimal('0.01'))
                        delivery_charge = fixed_charge + percentage_charge
                except:
                    delivery_charge = Decimal('2.50')  # Default

            total = subtotal + tax + delivery_charge

            # Associate order to authenticated user (do not trust client-provided user_id)
            user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None

            # Create order
            order = Order.objects.create(
                order_type=data['order_type'],
                status='pending',
                guest_name=data['guest_name'],
                guest_phone=data['guest_phone'],
                guest_email=data.get('guest_email', ''),
                special_requests=data.get('special_requests', ''),
                user=user,
                payment_method=data['payment_method'],
                payment_status='pending' if data['payment_method'] != 'cash' else 'unpaid',
                subtotal=subtotal,
                tax=tax,
                delivery_charge=delivery_charge,
                total_price=total
            )

            # Set order-type specific fields
            if data['order_type'] == 'seated':
                order.table_number = data.get('table_number')

            elif data['order_type'] == 'pickup':
                preferred_pickup_time_raw = data.get('preferred_pickup_time')
                if preferred_pickup_time_raw:
                    pickup_dt = parse_datetime(preferred_pickup_time_raw)
                    if pickup_dt is None:
                        return JsonResponse(
                            {
                                'success': False,
                                'message': 'Invalid preferred_pickup_time. Use ISO format, e.g. 2024-01-15T14:30'
                            },
                            status=400,
                        )

                    if timezone.is_naive(pickup_dt) and timezone.get_current_timezone() is not None:
                        pickup_dt = timezone.make_aware(pickup_dt, timezone.get_current_timezone())

                    order.preferred_pickup_time = pickup_dt

            elif data['order_type'] == 'delivery':
                order.delivery_address = data.get('delivery_address', '')
                order.delivery_city = data.get('delivery_city', '')
                order.delivery_postal_code = data.get('delivery_postal_code', '')
                delivery_country = data.get('delivery_country')
                if delivery_country:
                    order.delivery_country = delivery_country
                order.delivery_instructions = data.get('delivery_instructions', '')

            order.save()

            # Create order items
            for item_data in data['items']:
                try:
                    menu_item = MenuItem.objects.get(id=item_data.get('id'))
                except MenuItem.DoesNotExist:
                    menu_item = None

                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    item_name=item_data.get('name', 'Unknown Item'),
                    item_price=Decimal(str(item_data.get('price', 0))),
                    quantity=item_data.get('quantity', 1),
                    special_instructions=item_data.get('special_instructions', '')
                )

            # TODO: Handle payment processing based on payment method
            # For now, mark as pending for all methods

            logger.info(f"Order {order.id} created successfully for {data['guest_name']}")

            return JsonResponse({
                'success': True,
                'message': 'Order created successfully',
                'order_id': order.id,
                'total': str(total)
            })

    except Exception as e:
        logger.error(f"Error creating order: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'Error creating order: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_order_status(request, order_id):
    """
    GET /api/orders/{order_id}/
    Get order status and details
    """
    try:
        order = Order.objects.get(id=order_id)
        items = OrderItem.objects.filter(order=order).values()
        
        return JsonResponse({
            'id': order.id,
            'order_number': order.order_number,
            'status': order.status,
            'order_type': order.order_type,
            'guest_name': order.guest_name,
            'guest_phone': order.guest_phone,
            'guest_email': order.guest_email,
            'payment_status': order.payment_status,
            'payment_method': order.payment_method,
            'subtotal': str(order.subtotal),
            'tax': str(order.tax),
            'delivery_charge': str(order.delivery_charge),
            'total_price': str(order.total_price),
            'created_at': order.created_at.isoformat(),
            'estimated_completion_time': (order.estimated_completion_time.isoformat() 
                                         if order.estimated_completion_time else None),
            'items': list(items),
            'special_requests': order.special_requests
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching order: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
