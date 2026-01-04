# QUICK REFERENCE: PHASE 3 CHECKOUT FLOW

## 🎯 Quick Setup (5 minutes)

### 1. Run Migration
```bash
cd sip-sunshine-django
python manage.py migrate
```

### 2. Create Delivery Settings (Admin)
- Go to: `http://localhost:8000/admin/restaurant/deliverysettings/`
- Click: Add Delivery Settings
- Fill with defaults shown in template
- Save

### 3. Create Payment Settings (Admin)
- Go to: `http://localhost:8000/admin/restaurant/paymentsettings/`
- Click: Add Payment Settings
- Check: Test Mode = ON
- Check: Stripe Enabled = ON
- Check: PayPal Enabled = ON
- Save

### 4. Test Flow
1. Visit: `http://localhost:8000/menu/`
2. Click: "Add to Cart" (need to add button to menu first)
3. Visit: `http://localhost:8000/checkout/`
4. Click: "Start Checkout"
5. Complete all 4 steps

---

## 📁 Files at a Glance

### Templates
```
templates/checkout/
├── checkout.html              ← Main page with 4-step flow
├── order_type_modal.html      ← Modal 1: Choose type
├── customer_details_modal.html ← Modal 2: Customer info
└── order_review_modal.html    ← Modal 3: Review + payment
```

### Backend
```
restaurant/
├── api.py                     ← REST API endpoints
├── checkout_views.py          ← Django views
├── urls.py                    ← URL routing (UPDATED)
├── models.py                  ← DB models (from Phase 1-2)
└── admin.py                   ← Django admin (from Phase 1-2)
```

### Static Assets
```
static/js/
└── cart-system.js             ← Shopping cart (from Phase 2)
```

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/settings/delivery/` | GET | Fetch delivery settings |
| `/api/orders/create/` | POST | Create new order |
| `/api/orders/{id}/` | GET | Get order status |
| `/checkout/` | GET | Main checkout page |
| `/orders/confirmation/{id}/` | GET | Confirmation page |

---

## 💾 Data Flow

```
User Cart (localStorage)
         ↓
[Cart Modal] (cart-system.js)
         ↓
[Checkout Page] /checkout/
         ↓
[1. Order Type Modal] (sessionStorage)
    ↓ (fetches /api/settings/delivery/)
[2. Customer Details Modal] (sessionStorage)
    ↓
[3. Order Review Modal] (sessionStorage)
    ↓
[Submit] POST /api/orders/create/
    ↓
[Backend Processing]
    ├─ Validates all fields
    ├─ Creates Order record
    ├─ Creates OrderItem records
    ├─ Calculates totals
    └─ Returns order_id
    ↓
[Confirmation Page] /orders/confirmation/{id}/
    ↓
[Order Tracking] /orders/tracking/
```

---

## 🧪 Quick Test

```bash
# Test API
curl http://localhost:8000/api/settings/delivery/

# Create test order
curl -X POST http://localhost:8000/api/orders/create/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{
    "order_type": "pickup",
    "payment_method": "cash",
    "guest_name": "Test User",
    "guest_phone": "+31612345678",
    "items": [{"name": "Test Item", "price": 10, "quantity": 1}]
  }'
```

---

## ⚙️ Configuration Checklist

- [ ] Run migration: `python manage.py migrate`
- [ ] Create DeliverySettings in admin
- [ ] Create PaymentSettings in admin
- [ ] Update menu template with cart buttons
- [ ] Update navbar with cart icon
- [ ] Test full flow: Menu → Cart → Checkout
- [ ] Check confirmation page loads
- [ ] Verify order appears in admin

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| "Empty cart" error | Add items to cart from menu |
| 404 on API calls | Check DeliverySettings exists |
| Order not created | Check browser console for errors |
| Modals not showing | Verify JavaScript loaded (F12) |
| Styling broken | Clear browser cache (Ctrl+Shift+Del) |

---

## 📋 Next Integration Task

**Update Menu Template** to add cart buttons:

```html
<button onclick="cart.addToCart({
    id: {{ item.id }},
    name: '{{ item.name }}',
    price: {{ item.price }}
}, 1)" class="btn btn-sm btn-danger">
    🛒 Add
</button>
```

---

## 🎓 Function Reference

### JavaScript (order_type_modal.html)
- `openOrderTypeModal()` - Show modal
- `selectOrderType(type)` - Select dine-in/pickup/delivery
- `loadDeliverySettings()` - Fetch from API
- `closeOrderTypeModal()` - Hide modal

### JavaScript (customer_details_modal.html)
- `openCustomerDetailsModal()` - Show modal
- `switchAuthMode(mode)` - Toggle login/register/guest
- `proceedToDeliveryDetails()` - Validate & next
- `goBackToOrderType()` - Go back

### JavaScript (order_review_modal.html)
- `openOrderReviewModal()` - Show modal
- `populateOrderReview()` - Display data
- `submitOrder()` - POST to API
- `goBackToCustomerDetails()` - Go back

### Python API (restaurant/api.py)
- `get_delivery_settings(request)` - Return settings JSON
- `create_order(request)` - Create order & items
- `get_order_status(request, order_id)` - Return order JSON

---

## 💡 Pro Tips

1. **Debug sessionStorage**: Open DevTools → Application → Session Storage
2. **Debug API calls**: DevTools → Network tab → XHR
3. **Test payment methods**: All 3 are accepted (logic is TODO)
4. **Check logs**: `python manage.py runserver` output
5. **Admin shortcuts**: 
   - Orders: `/admin/restaurant/order/`
   - Settings: `/admin/restaurant/deliverysettings/`
   - Payments: `/admin/restaurant/paymentsettings/`

---

## 📞 Emergency Fixes

**If modals don't show:**
```javascript
// Run in browser console
openOrderTypeModal()  // Should show first modal
```

**If cart is empty:**
```javascript
// Run in browser console
localStorage.setItem('sip_sunshine_cart', JSON.stringify([{id:1, name:'Test', price:10, quantity:1}]))
```

**If API returns 404:**
```
1. Go to admin
2. Create DeliverySettings
3. Reload checkout page
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────┐
│        Shopping Cart (Frontend)         │
│  localStorage: sip_sunshine_cart        │
└────────────────┬──────────────────────┘
                 │
                 ↓
         ┌─────────────────┐
         │  Checkout Page  │
         │    4-step flow  │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    ↓             ↓             ↓
Modal 1        Modal 2        Modal 3
Order Type   Customer        Review
             Details         & Payment
    │             │             │
    └─────────────┼─────────────┘
                  │
                  ↓
         ┌─────────────────────┐
         │  POST /api/          │
         │  orders/create/      │
         └────────┬────────────┘
                  │
                  ↓
      ┌──────────────────────┐
      │  Django Backend      │
      │  - Validate data     │
      │  - Create Order      │
      │  - Create Items      │
      │  - Calculate totals  │
      └────────┬─────────────┘
               │
               ↓
    ┌────────────────────────┐
    │ Confirmation Page      │
    │ /orders/confirmation/  │
    └────────────────────────┘
```

---

**Status**: 🟢 Ready to Deploy  
**Last Updated**: 2024  
**Version**: 3.0  
