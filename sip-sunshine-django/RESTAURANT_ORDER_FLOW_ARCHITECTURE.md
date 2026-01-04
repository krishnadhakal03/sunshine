# Restaurant Order System - Complete Architecture & Design

## Executive Summary
Redesign the order flow to match standard restaurant operations with shopping cart, order type selection (Dine-In/Pickup/Delivery), and flexible checkout supporting both registered and guest users.

---

## 1. SYSTEM ARCHITECTURE

### 1.1 Database Models (Django)

#### New/Modified Models:

**A. Order Model Changes**
```python
class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('seated', 'Seated at Table'),
        ('pickup', 'Pickup Order'),
        ('delivery', 'Delivery Order'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Existing fields
    id = AutoField(primary_key=True)
    order_type = CharField(choices=ORDER_TYPE_CHOICES)  # ADD: 'pickup'
    status = CharField(choices=STATUS_CHOICES)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    # Guest/Customer info
    guest_name = CharField(max_length=100)
    guest_email = EmailField()
    guest_phone = CharField(max_length=15)
    
    # Seated order
    table_number = IntegerField(null=True, blank=True)
    
    # Pickup/Delivery address
    delivery_address = CharField(max_length=255, null=True, blank=True)
    delivery_city = CharField(max_length=100, null=True, blank=True)
    delivery_postal_code = CharField(max_length=10, null=True, blank=True)
    delivery_country = CharField(max_length=100, null=True, blank=True)
    
    # NEW: Delivery details
    delivery_charge = DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_delivery_time = IntegerField(null=True, blank=True)  # minutes
    
    # NEW: Payment info
    payment_method = CharField(max_length=50, choices=[
        ('cash', 'Cash on Delivery'),
        ('card', 'Card Payment'),
        ('wallet', 'Digital Wallet'),
    ], default='cash')
    payment_status = CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    
    # NEW: Order timing
    promised_time = DateTimeField(null=True, blank=True)
    completed_at = DateTimeField(null=True, blank=True)
    
    # Pricing
    subtotal = DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = DecimalField(max_digits=10, decimal_places=2)
    
    # Notes
    special_requests = TextField(blank=True)
    
    # NEW: User linking (optional for guest orders)
    user = ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

class OrderItem(models.Model):
    order = ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item_name = CharField(max_length=100)
    item_price = DecimalField(max_digits=10, decimal_places=2)
    quantity = IntegerField()
    special_instructions = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**B. New Cart Model (Server-side session backup)**
```python
class Cart(models.Model):
    session_key = CharField(max_length=40, unique=True)
    user = ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    items = JSONField(default=list)  # [{item_id, name, price, qty, image, desc}]
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Shopping Cart"
```

**C. Delivery Settings Model**
```python
class DeliverySettings(models.Model):
    delivery_enabled = BooleanField(default=True)
    pickup_enabled = BooleanField(default=True)
    delivery_charge_fixed = DecimalField(max_digits=10, decimal_places=2, default=2.50)
    delivery_charge_percent = DecimalField(max_digits=5, decimal_places=2, default=0)  # % of order
    min_delivery_amount = DecimalField(max_digits=10, decimal_places=2, default=10)
    estimated_pickup_time = IntegerField(default=15)  # minutes
    estimated_delivery_time = IntegerField(default=30)  # minutes
    max_delivery_radius = DecimalField(max_digits=5, decimal_places=2, default=5)  # km
```

---

## 2. USER FLOW - COMPLETE JOURNEY

### Phase 1: Shopping Cart
```
Menu Page
  ↓
User sees items → "Add to Cart" button (instead of "Add to Order")
  ↓
Toast notification: "Item added to cart"
  ↓
Cart icon shows count badge
  ↓
User can: Continue shopping OR View Cart
```

### Phase 2: View Cart
```
Cart Modal/Page shows:
  ├─ All cart items with:
  │  ├─ Item image
  │  ├─ Item name & description
  │  ├─ Price per unit
  │  ├─ Quantity (±buttons)
  │  ├─ Subtotal per item
  │  └─ Remove button
  ├─ Cart Summary:
  │  ├─ Subtotal
  │  ├─ Tax (if applicable)
  │  └─ Total
  └─ Action Buttons:
     ├─ Continue Shopping
     └─ Proceed to Checkout
```

### Phase 3: Order Type Selection
```
"Order Type" Selection:
  ├─ 🪑 Dine-In (Seated at Table)
  │   └─ Shows: Table number field
  │
  ├─ 🛒 Pickup
  │   └─ Shows: Estimated pickup time (e.g., "Ready in 30 min")
  │            Pickup instructions (if any)
  │
  └─ 🚚 Delivery
      └─ Shows: Delivery address form
               Estimated delivery time
               Delivery charge
               ⚠️ Warning if address outside service area
```

### Phase 4: Customer Information
```
Registration/Login Check:
  ├─ IF logged in → Skip to "Delivery Details"
  ├─ IF not logged in → Show options:
  │   ├─ Option A: "Register & Login" (full account)
  │   ├─ Option B: "Guest Checkout" (continue as guest)
  │   └─ Option C: "Social Login" (Google/Facebook if configured)
  └─ Continue
```

### Phase 5: Enter/Confirm Details
```
For Dine-In:
  ├─ Name (required)
  ├─ Email (optional)
  ├─ Phone (required)
  ├─ Table Number (required)
  └─ Special Requests (optional)

For Pickup:
  ├─ Name (required)
  ├─ Email (optional)
  ├─ Phone (required)
  ├─ Preferred Pickup Time (optional)
  └─ Special Requests (optional)

For Delivery:
  ├─ Name (required)
  ├─ Email (optional)
  ├─ Phone (required)
  ├─ Delivery Address (required)
  ├─ City (required)
  ├─ Postal Code (required)
  ├─ Delivery Instructions (optional)
  └─ Special Requests (optional)
```

### Phase 6: Order Review & Payment
```
Order Summary Screen:
  ├─ Order Items (read-only list)
  ├─ Subtotal
  ├─ Delivery Charge (if applicable)
  ├─ Tax
  ├─ TOTAL
  ├─ Order Type & Details
  └─ Payment Method Selection:
     ├─ Radio: "Cash on Delivery/Pickup"
     ├─ Radio: "Card Payment" (Stripe/PayPal - optional)
     └─ Radio: "Digital Wallet" (optional)
```

### Phase 7: Payment Processing
```
IF Cash on Delivery/Pickup:
  └─ Show: "Confirm Order" button
     ├─ Submit order to backend
     └─ Show confirmation screen

IF Card Payment:
  └─ Redirect to payment gateway (Stripe/PayPal)
     ├─ Process payment
     └─ Return to confirmation
```

### Phase 8: Order Confirmation
```
Confirmation Screen:
  ├─ ✅ "Order Confirmed!"
  ├─ Order ID: #12345
  ├─ Order Type: Delivery
  ├─ Estimated Time: "Today at 7:45 PM"
  ├─ Total Amount: €45.50
  ├─ Delivery Address (if applicable)
  ├─ Actions:
  │  ├─ "Track Order" (redirects to tracking page)
  │  ├─ "Download Invoice"
  │  └─ "Continue Shopping"
  └─ Email confirmation sent to guest_email
```

---

## 3. API ENDPOINTS (Django Rest Framework or Traditional Views)

### Cart Operations
```
POST   /api/cart/add/              - Add item to cart
GET    /api/cart/                  - Get cart items
POST   /api/cart/update/           - Update item quantity
DELETE /api/cart/remove/{item_id}/ - Remove item
POST   /api/cart/clear/            - Clear entire cart
```

### Order Operations
```
POST   /api/orders/create/         - Create order (checkout)
GET    /api/orders/{order_id}/     - Get order details
GET    /api/orders/my-orders/      - Get user's orders
POST   /api/orders/{order_id}/track/ - Track order status
```

### Payment Operations
```
POST   /api/payments/process/      - Process payment (if integrated)
POST   /api/payments/verify/       - Verify payment status
```

### Settings
```
GET    /api/settings/delivery/     - Get delivery settings
GET    /api/settings/restaurants/  - Get restaurant info
```

---

## 4. FRONTEND TEMPLATES & COMPONENTS

### New Templates to Create:
```
templates/
├── cart/
│   ├── cart_modal.html          - Shopping cart modal
│   └── cart_page.html           - Full cart page (optional)
├── checkout/
│   ├── order_type_selection.html - Choose: Dine-In/Pickup/Delivery
│   ├── customer_details.html     - Enter customer info
│   ├── delivery_details.html     - Address & delivery options
│   ├── order_review.html         - Final review & payment
│   └── confirmation.html         - Order confirmed
├── auth/
│   ├── guest_checkout.html       - Guest checkout prompt
│   └── quick_login.html          - Quick login/register
└── orders/
    ├── order_tracking.html       - Track order status
    └── order_history.html        - View past orders
```

### Modify Existing Templates:
```
templates/pages/menu.html
  - Replace "Add to Order" with "Add to Cart"
  - Replace modal with cart management
  
templates/base.html / navbar
  - Add cart icon with item count badge
```

---

## 5. JAVASCRIPT FUNCTIONALITY

### New JS Files:
```
static/js/
├── cart-system.js               - Shopping cart management
│   ├── addToCart()
│   ├── removeFromCart()
│   ├── updateQuantity()
│   ├── getCartTotal()
│   ├── displayCart()
│   └── syncCartWithServer()
│
├── checkout-flow.js             - Checkout process
│   ├── selectOrderType()
│   ├── validateDeliveryAddress()
│   ├── calculateDeliveryCharge()
│   ├── validateCustomerDetails()
│   └── submitOrder()
│
└── payment-processor.js          - Payment handling (if needed)
    ├── processCardPayment()
    └── handlePaymentResponse()
```

---

## 6. IMPLEMENTATION ROADMAP

### Phase 1: Database & Models (1-2 hours)
- [ ] Modify Order model (add pickup, delivery_charge, payment_method)
- [ ] Create Cart model
- [ ] Create DeliverySettings model
- [ ] Run migrations

### Phase 2: Shopping Cart (2-3 hours)
- [ ] Create cart-system.js
- [ ] Create Cart API endpoints
- [ ] Create cart modal template
- [ ] Modify menu.html "Add to Order" → "Add to Cart"
- [ ] Add cart icon to navbar

### Phase 3: Order Type Selection (2 hours)
- [ ] Create order type selection modal/page
- [ ] Conditional field display (table/address/pickup time)
- [ ] Validate selections

### Phase 4: Authentication & Guest Checkout (2-3 hours)
- [ ] Create guest checkout prompt
- [ ] Implement quick login/register
- [ ] Handle session management for guests

### Phase 5: Delivery Details & Validation (2 hours)
- [ ] Address validation
- [ ] Delivery charge calculation
- [ ] Service area validation

### Phase 6: Order Review & Confirmation (2 hours)
- [ ] Create order review template
- [ ] Implement order submission
- [ ] Create confirmation template
- [ ] Email notifications

### Phase 7: Payment Integration (Optional, 3-4 hours)
- [ ] Integrate Stripe/PayPal (optional)
- [ ] Handle payment success/failure
- [ ] Payment status tracking

### Phase 8: Testing & Polish (2 hours)
- [ ] End-to-end testing
- [ ] Mobile responsiveness
- [ ] Error handling

---

## 7. KEY DESIGN DECISIONS

### Cart Storage
**Hybrid Approach:**
- **Client-side (localStorage)**: Fast, instant updates, survives session
- **Server-side (Database)**: Backup for registered users, sync between devices
- **Sync Logic**: Save to server every 30 seconds or on significant changes

### Delivery Charge Calculation
```javascript
if (orderType === 'delivery') {
    let charge = 0;
    
    // Option 1: Fixed charge
    charge += DELIVERY_SETTINGS.delivery_charge_fixed;
    
    // Option 2: Percentage-based
    charge += (cartTotal * DELIVERY_SETTINGS.delivery_charge_percent) / 100;
    
    // Apply minimum order value
    if (cartTotal < DELIVERY_SETTINGS.min_delivery_amount) {
        showWarning(`Minimum delivery order: €${MIN_DELIVERY}`);
    }
    
    return charge;
}
```

### Guest vs Registered User
```
Guest Order Flow:
  - Enter name, email, phone
  - No password needed
  - Order tracked via email link or order ID
  - Option to register after checkout

Registered User:
  - Auto-fill saved addresses
  - Saved payment methods
  - Loyalty points (if applicable)
  - Order history
```

### Status Flow for Each Order Type
```
Dine-In: Pending → Confirmed → Preparing → Ready → Completed
         (waiter notified when ready)

Pickup: Pending → Confirmed → Preparing → Ready → Completed
        (customer notified when ready)

Delivery: Pending → Confirmed → Preparing → Out for Delivery → Completed
          (real-time tracking if GPS enabled)
```

---

## 8. MOCKUP/UI FLOW VISUALIZATION

```
[Menu Page]
    ↓ (Add to Cart)
    ↓
[Shopping Cart Modal]
    ├─ Item 1: €12.50 x2 = €25.00
    ├─ Item 2: €8.50 x1 = €8.50
    └─ [Total: €33.50] [Checkout]
    ↓
[Order Type Selection]
    ├─ 🪑 Dine-In
    ├─ 🛒 Pickup
    └─ 🚚 Delivery
    ↓
[Customer Details] (varies by order type)
    ├─ Name *
    ├─ Phone *
    ├─ [Table# / Address / Pickup Time]
    └─ [Next]
    ↓
[Login/Register or Continue as Guest]
    ├─ Register
    ├─ Login
    └─ Continue as Guest
    ↓
[Order Review & Payment]
    ├─ Items: €33.50
    ├─ Delivery: €2.50 (if applicable)
    ├─ Tax: €6.70
    ├─ Total: €42.70
    ├─ Payment Method: [Cash / Card / Wallet]
    └─ [Confirm Order]
    ↓
[Order Confirmation]
    ├─ ✅ Order #12345
    ├─ Status: Confirmed
    ├─ Est. Time: 30 min
    └─ [Track] [Invoice] [Home]
```

---

## 9. SECURITY CONSIDERATIONS

- ✅ CSRF protection on all forms
- ✅ Validate delivery address (prevent abuse)
- ✅ Rate limiting on order creation
- ✅ Encrypt sensitive data (addresses, phone)
- ✅ Validate payment amounts server-side
- ✅ Audit logging for all orders
- ✅ PCI compliance if handling cards

---

## 10. FUTURE ENHANCEMENTS

1. **Real-time Order Tracking** - WebSocket updates
2. **Loyalty Program** - Points & rewards
3. **Multi-location Support** - Multiple restaurants
4. **Advanced Analytics** - Peak hours, popular items
5. **Rating & Reviews** - Post-order feedback
6. **Subscription Orders** - Recurring orders
7. **Promo Codes** - Discount management
8. **Kitchen Display System (KDS)** - Backend order management

---

## NEXT STEPS

Shall I proceed with implementation? I recommend starting with:

1. **Phase 1-2**: Database models + Shopping Cart (foundation)
2. **Phase 3-4**: Order flow + Authentication  
3. **Phase 5-6**: Checkout + Confirmation
4. **Phase 7**: Payment (optional)

**Should I start building?** ✅ YES / CONFIRM FIRST?
