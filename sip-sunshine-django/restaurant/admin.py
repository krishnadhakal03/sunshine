from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from parler.admin import TranslatableAdmin
from .models import (
    Language, SiteSetting, Page, MenuItem, ContentBlock,
    BlogPost, Reservation, ContactMessage, Order, OrderItem,
    Cart, DeliverySettings, PaymentSettings
)



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('get_flag', 'name', 'code', 'get_active_status', 'is_active', 'is_default')
    list_editable = ('is_active', 'is_default')
    list_filter = ('is_active', 'is_default')
    search_fields = ('name', 'code')
    
    def get_flag(self, obj):
        flags = {'en': '🇬🇧', 'nl': '🇳🇱', 'fr': '🇫🇷'}
        return flags.get(obj.code, '🌐')
    get_flag.short_description = 'Language'
    
    def get_active_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Active</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Inactive</span>')
    get_active_status.short_description = 'Status'


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('site_name', 'site_description', 'site_keywords', 'site_logo', 'site_favicon')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'address')
        }),
        (_('Social Media'), {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url')
        }),
        (_('Location'), {
            'fields': ('google_map_embed',)
        }),
    )
    
    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    list_display = ('title', 'template_name', 'is_homepage', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('template_name', 'is_active', 'is_homepage')
    search_fields = ('title', 'slug')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('slug', 'template_name', 'is_homepage', 'is_active', 'order')
        }),
        (_('Content'), {
            'fields': ('title', 'content')
        }),
        (_('SEO Settings'), {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MenuItem)
class MenuItemAdmin(TranslatableAdmin):
    list_display = ('get_thumbnail', 'name', 'category', 'get_price', 'get_status', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('category', 'order')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'category', 'price')
        }),
        (_('Content'), {
            'fields': ('description',)
        }),
        (_('Image'), {
            'fields': ('image',),
            'description': 'Upload a high-quality image (recommended: 400x300px)'
        }),
        (_('Settings'), {
            'fields': ('is_active', 'order')
        }),
    )
    
    def get_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 4px; object-fit: cover;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No image</span>')
    get_thumbnail.short_description = 'Image'
    
    def get_price(self, obj):
        return format_html('<span style="color: #f34949; font-weight: bold;">€{}</span>', obj.price)
    get_price.short_description = 'Price'
    
    def get_status(self, obj):
        if obj.is_active:
            return format_html('<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Active</span>')
        return format_html('<span style="background: #dc3545; color: white; padding: 3px 8px; border-radius: 3px;">Inactive</span>')
    get_status.short_description = 'Status'


@admin.register(ContentBlock)
class ContentBlockAdmin(TranslatableAdmin):
    list_display = ('key', 'block_type', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('block_type', 'is_active')
    search_fields = ('key', 'title')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('key', 'block_type', 'image', 'order', 'is_active')
        }),
        (_('Content'), {
            'fields': ('title', 'subtitle', 'content')
        }),
        (_('Button'), {
            'fields': ('button_text', 'button_url'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogPost)
class BlogPostAdmin(TranslatableAdmin):
    list_display = ('title', 'author', 'is_published', 'published_at', 'created_at')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'content', 'author')
    date_hierarchy = 'published_at'
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'author', 'featured_image')
        }),
        (_('Content'), {
            'fields': ('excerpt', 'content')
        }),
        (_('Publication'), {
            'fields': ('is_published', 'published_at')
        }),
        (_('SEO Settings'), {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('get_guest_info', 'get_reservation_details', 'get_status_badge', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'reservation_date', 'created_at')
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'reservation_date'
    readonly_fields = ('created_at', 'get_guest_contact')
    
    fieldsets = (
        (_('Guest Information'), {
            'fields': ('name', 'email', 'phone', 'get_guest_contact')
        }),
        (_('Reservation Details'), {
            'fields': ('reservation_date', 'reservation_time', 'number_of_guests')
        }),
        (_('Status & Notes'), {
            'fields': ('status', 'special_requests', 'created_at')
        }),
    )
    
    def get_guest_info(self, obj):
        return format_html(
            '<strong>{}</strong><br/><small style="color: #666;">{}</small>',
            obj.name,
            obj.email
        )
    get_guest_info.short_description = 'Guest'
    
    def get_reservation_details(self, obj):
        return format_html(
            '<strong>{} at {}</strong><br/><small>👥 {} Guests</small>',
            obj.reservation_date.strftime('%b %d, %Y'),
            obj.reservation_time.strftime('%H:%M'),
            obj.number_of_guests
        )
    get_reservation_details.short_description = 'Reservation'
    
    def get_status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'cancelled': '#dc3545',
            'completed': '#17a2b8'
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    get_status_badge.short_description = 'Status'
    
    def get_guest_contact(self, obj):
        return format_html(
            '<strong>Email:</strong> {}<br/><strong>Phone:</strong> {}',
            obj.email,
            obj.phone
        )
    get_guest_contact.short_description = 'Contact Information'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('get_contact_info', 'get_subject_preview', 'get_read_status', 'is_read', 'created_at')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'get_full_contact')
    
    fieldsets = (
        (_('Contact Information'), {
            'fields': ('name', 'email', 'phone', 'get_full_contact')
        }),
        (_('Message'), {
            'fields': ('subject', 'message')
        }),
        (_('Status'), {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def get_contact_info(self, obj):
        return format_html(
            '<strong>{}</strong><br/><small style="color: #666;">{}</small>',
            obj.name,
            obj.email
        )
    get_contact_info.short_description = 'From'
    
    def get_subject_preview(self, obj):
        preview = obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
        return format_html('<em>{}</em>', preview)
    get_subject_preview.short_description = 'Subject'
    
    def get_read_status(self, obj):
        if obj.is_read:
            return format_html('<span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Read</span>')
        return format_html('<span style="background: #ffc107; color: #333; padding: 3px 8px; border-radius: 3px;">⚡ New</span>')
    get_read_status.short_description = 'Status'
    
    def get_full_contact(self, obj):
        return format_html(
            '<strong>Name:</strong> {}<br/><strong>Email:</strong> {}<br/><strong>Phone:</strong> {}',
            obj.name,
            obj.email,
            obj.phone
        )
    get_full_contact.short_description = 'Contact Details'
    
    def has_add_permission(self, request):
        return False


# ==================== Order Management ====================

class OrderItemInline(admin.TabularInline):
    """Inline Order Items in Order admin"""
    model = OrderItem
    extra = 0
    readonly_fields = ('created_at', 'get_subtotal')
    fields = ('item_name', 'item_price', 'quantity', 'special_instructions', 'get_subtotal', 'created_at')
    
    def get_subtotal(self, obj):
        return format_html(
            '<strong style="color: #f34949;">€{}</strong>',
            obj.get_subtotal()
        )
    get_subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_order_info', 'get_customer_info', 'get_order_type_badge', 'get_payment_status', 'get_total', 'created_at')
    list_editable = ()
    list_filter = ('status', 'order_type', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('guest_name', 'guest_email', 'guest_phone', 'id', 'payment_id')
    date_hierarchy = 'created_at'
    readonly_fields = ('id', 'created_at', 'updated_at', 'get_order_summary', 'subtotal', 'tax')
    inlines = [OrderItemInline]
    
    fieldsets = (
        (_('Order Information'), {
            'fields': ('id', 'order_type', 'status', 'created_at', 'updated_at')
        }),
        (_('Customer Details'), {
            'fields': ('user', 'guest_name', 'guest_email', 'guest_phone')
        }),
        (_('Seated Order'), {
            'fields': ('table_number',),
            'classes': ('collapse',)
        }),
        (_('Pickup Order'), {
            'fields': ('preferred_pickup_time',),
            'classes': ('collapse',)
        }),
        (_('Delivery Order'), {
            'fields': (
                'delivery_address', 'delivery_city', 'delivery_postal_code', 'delivery_country',
                'delivery_instructions', 'delivery_charge', 'estimated_delivery_time'
            ),
            'classes': ('collapse',)
        }),
        (_('Pricing'), {
            'fields': ('subtotal', 'tax', 'total_price')
        }),
        (_('Payment Information'), {
            'fields': ('payment_method', 'payment_status', 'payment_id', 'payment_details')
        }),
        (_('Special Requests'), {
            'fields': ('special_requests',),
            'classes': ('wide',)
        }),
        (_('Order Timing'), {
            'fields': ('promised_time', 'completed_at')
        }),
    )
    
    def get_order_info(self, obj):
        return format_html(
            '<strong>Order #{}</strong><br/><small style="color: #999;">{}</small>',
            obj.id,
            obj.created_at.strftime('%b %d, %Y %H:%M')
        )
    get_order_info.short_description = 'Order'
    
    def get_customer_info(self, obj):
        if obj.user:
            return format_html(
                '<strong>{}</strong><br/><small style="color: #666;">{}</small>',
                obj.user.get_full_name() or obj.user.username,
                obj.user.email
            )
        return format_html(
            '<strong>{}</strong><br/><small style="color: #666;">{}</small>',
            obj.guest_name,
            obj.guest_email or obj.guest_phone or '-'
        )
    get_customer_info.short_description = 'Customer'
    
    def get_order_type_badge(self, obj):
        colors = {
            'seated': '#17a2b8',
            'pickup': '#20c997',
            'delivery': '#ffc107',
        }
        color = colors.get(obj.order_type, '#999')
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_order_type_display()
        )
    get_order_type_badge.short_description = 'Type'
    
    def get_payment_status(self, obj):
        colors = {
            'pending': '#ffc107',
            'completed': '#28a745',
            'failed': '#dc3545',
            'refunded': '#6f42c1',
        }
        color = colors.get(obj.payment_status, '#999')
        icon = {
            'pending': '⏳',
            'completed': '✅',
            'failed': '❌',
            'refunded': '↩️',
        }
        return format_html(
            '{} <span style="background: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            icon.get(obj.payment_status, ''),
            color,
            obj.get_payment_status_display()
        )
    get_payment_status.short_description = 'Payment'

    get_customer_info.short_description = 'Customer'
    
    def get_status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'preparing': '#17a2b8',
            'ready': '#20c997',
            'completed': '#28a745',
            'cancelled': '#dc3545'
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    get_status_badge.short_description = 'Status'
    
    def get_total(self, obj):
        return format_html(
            '<span style="color: #f34949; font-weight: bold;">€{}</span>',
            obj.total_price
        )
    get_total.short_description = 'Total'
    
    def get_order_summary(self, obj):
        items = obj.items.all()
        items_html = '<br/>'.join([
            f"• {item.item_name} x{item.quantity} - €{item.get_subtotal()}"
            for item in items
        ])
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px; border-radius: 4px;"><strong>Items:</strong><br/>{}<hr/><strong>Total:</strong> €{}</div>',
            items_html,
            obj.total_price
        )
    get_order_summary.short_description = 'Order Summary'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('get_item_info', 'quantity', 'item_price', 'get_subtotal', 'order_link')
    list_filter = ('created_at', 'item_price')
    search_fields = ('item_name', 'order__guest_name', 'special_instructions')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'order')
    
    def get_item_info(self, obj):
        return format_html(
            '<strong>{}</strong><br/><small style="color: #999;">{}</small>',
            obj.item_name,
            obj.special_instructions[:50] if obj.special_instructions else 'No special instructions'
        )
    get_item_info.short_description = 'Item'
    
    def get_subtotal(self, obj):
        return format_html(
            '<span style="color: #f34949; font-weight: bold;">€{}</span>',
            obj.get_subtotal()
        )
    get_subtotal.short_description = 'Subtotal'
    
    def order_link(self, obj):
        return format_html(
            '<a href="/admin/restaurant/order/{}/change/">Order #{}</a>',
            obj.order.id,
            obj.order.id
        )
    order_link.short_description = 'Order'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Shopping Cart Administration"""
    list_display = ('get_user_info', 'get_item_count', 'get_total', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('session_key', 'user__username', 'user__email')
    readonly_fields = ('session_key', 'created_at', 'updated_at', 'items')
    
    def get_user_info(self, obj):
        if obj.user:
            return format_html(
                '<strong>{}</strong><br/><small>{}</small>',
                obj.user.username,
                obj.user.email
            )
        return f'Guest: {obj.session_key[:20]}...'
    get_user_info.short_description = 'User/Session'
    
    def get_item_count(self, obj):
        try:
            items = obj.items if isinstance(obj.items, list) else []
            count = sum(item.get('quantity', 1) for item in items)
            return count
        except:
            return 0
    get_item_count.short_description = 'Items'
    
    def get_total(self, obj):
        total = obj.get_total()
        return format_html('<span style="color: #f34949; font-weight: bold;">€{}</span>', total)
    get_total.short_description = 'Total'


@admin.register(DeliverySettings)
class DeliverySettingsAdmin(admin.ModelAdmin):
    """Delivery & Pickup Settings"""
    fieldsets = (
        (_('Service Availability'), {
            'fields': ('delivery_enabled', 'pickup_enabled')
        }),
        (_('Delivery Charges'), {
            'fields': ('delivery_charge_fixed', 'delivery_charge_percent', 'min_delivery_amount')
        }),
        (_('Pickup Settings'), {
            'fields': ('min_pickup_amount', 'estimated_pickup_time')
        }),
        (_('Delivery Timing & Area'), {
            'fields': ('estimated_delivery_time', 'max_delivery_radius')
        }),
        (_('Operating Hours'), {
            'fields': (
                'delivery_start_time', 'delivery_end_time',
                'pickup_start_time', 'pickup_end_time'
            )
        }),
    )
    
    def has_add_permission(self, request):
        return not DeliverySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    """Payment Gateway Settings"""
    fieldsets = (
        (_('Gateway Configuration'), {
            'fields': ('gateway', 'enabled', 'is_test_mode')
        }),
        (_('Stripe Settings'), {
            'fields': ('stripe_public_key', 'stripe_secret_key'),
            'classes': ('collapse',),
            'description': 'Get keys from <a href="https://dashboard.stripe.com" target="_blank">Stripe Dashboard</a>'
        }),
        (_('PayPal Settings'), {
            'fields': ('paypal_client_id', 'paypal_secret'),
            'classes': ('collapse',),
            'description': 'Get credentials from <a href="https://developer.paypal.com" target="_blank">PayPal Developer</a>'
        }),
    )
    list_display = ('get_gateway_name', 'enabled', 'is_test_mode', 'updated_at')
    list_editable = ('enabled', 'is_test_mode')
    list_filter = ('gateway', 'enabled', 'is_test_mode')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_gateway_name(self, obj):
        status = '✅' if obj.enabled else '❌'
        return format_html('{} {}', status, obj.get_gateway_display())
    get_gateway_name.short_description = 'Payment Gateway'

