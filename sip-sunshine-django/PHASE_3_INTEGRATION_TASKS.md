# PHASE 3: INTEGRATION TASKS

## What Needs to Be Updated in Existing Templates

### 1. BASE.html - Add Cart JavaScript & Navbar Button

**Location**: `templates/base.html`

**Add to `<head>` section:**
```html
<!-- Shopping Cart System -->
<script src="{% static 'js/cart-system.js' %}"></script>
```

**Add to navbar (usually in top navigation):**
```html
<!-- Cart Icon with Badge -->
<div style="display: flex; align-items: center; gap: 10px;">
    <button onclick="cart.openCartModal()" style="
        position: relative;
        background: transparent;
        border: 2px solid #f34949;
        color: #f34949;
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s;
    " onmouseover="this.style.background='rgba(243,73,73,0.1)';" onmouseout="this.style.background='transparent';">
        🛒 Cart
        <span id="cartBadge" style="
            position: absolute;
            top: -8px;
            right: -8px;
            background: #f34949;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            min-width: 24px;
        ">0</span>
    </button>
    
    <a href="{% url 'restaurant:checkout' %}" class="btn" style="
        background: linear-gradient(135deg, #f34949 0%, #d63d3d 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s;
    " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 5px 15px rgba(243,73,73,0.3)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
        🛍️ Checkout
    </a>
</div>
```

---

### 2. MENU.html - Add Cart Buttons to Items

**Location**: `templates/restaurant/menu.html` (or equivalent menu template)

**Find the menu item display loop and add this button:**

```html
<!-- Menu Item Card Template -->
<div class="menu-item">
    <h5>{{ item.name }}</h5>
    <p>{{ item.description }}</p>
    <p class="price">€{{ item.price }}</p>
    
    <!-- Add to Cart Button -->
    <button onclick="cart.addToCart({
        id: {{ item.id }},
        name: '{{ item.name }}',
        price: {{ item.price }},
        description: '{{ item.description|escapejs }}'
    }, 1)" class="btn btn-sm" style="
        background: linear-gradient(135deg, #f34949 0%, #d63d3d 100%);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 5px 15px rgba(243,73,73,0.3)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
        🛒 Add to Cart
    </button>
</div>
```

**Alternative for Bootstrap/Card layouts:**
```html
<div class="card">
    <div class="card-body">
        <h5 class="card-title">{{ item.name }}</h5>
        <p class="card-text">{{ item.description }}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
            <span style="font-size: 18px; font-weight: 700; color: #f34949;">€{{ item.price }}</span>
            <button onclick="cart.addToCart({id: {{ item.id }}, name: '{{ item.name }}', price: {{ item.price }}}, 1)" class="btn btn-sm btn-danger">
                🛒 Add
            </button>
        </div>
    </div>
</div>
```

---

### 3. CHECKOUT.html - Already Complete ✅

The checkout page is already created at:
- **File**: `templates/checkout/checkout.html`
- **Route**: `/checkout/`
- **Status**: Ready to use

No updates needed - it includes all 4 modals and flows.

---

## Integration Verification Checklist

- [ ] Cart JavaScript loaded in base.html
- [ ] Cart icon appears in navbar
- [ ] Checkout button in navbar links to `/checkout/`
- [ ] Menu items have "Add to Cart" buttons
- [ ] Clicking "Add to Cart" opens modal or shows toast
- [ ] Cart badge updates with item count
- [ ] Clicking cart icon opens cart modal
- [ ] Cart modal shows items
- [ ] "Proceed to Checkout" button works
- [ ] Checkout page loads at `/checkout/`
- [ ] All 4 modals appear in sequence
- [ ] Order can be submitted
- [ ] Confirmation page displays

---

## Code Snippets for Quick Copy-Paste

### Navbar Integration
```html
<!-- In your navbar/header template -->
<div class="navbar-item">
    <button onclick="cart.openCartModal()" class="nav-btn cart-btn">
        🛒 Cart <span id="cartBadge" class="badge">0</span>
    </button>
    <a href="/checkout/" class="nav-btn checkout-btn">🛍️ Checkout</a>
</div>

<style>
    .nav-btn {
        padding: 8px 16px;
        border-radius: 6px;
        border: none;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .cart-btn {
        background: transparent;
        border: 2px solid #f34949;
        color: #f34949;
    }
    
    .cart-btn:hover {
        background: rgba(243, 73, 73, 0.1);
    }
    
    .checkout-btn {
        background: linear-gradient(135deg, #f34949 0%, #d63d3d 100%);
        color: white;
        text-decoration: none;
    }
    
    .checkout-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(243, 73, 73, 0.3);
    }
    
    .badge {
        position: relative;
        top: -2px;
        left: 5px;
        background: #f34949;
        color: white;
        padding: 2px 6px;
        border-radius: 12px;
        font-size: 11px;
    }
</style>
```

### Menu Item Integration
```html
<!-- In your menu items loop -->
{% for item in menu_items %}
    <div class="menu-item">
        <div class="menu-item-header">
            <h4>{{ item.name }}</h4>
            <span class="price">€{{ item.price }}</span>
        </div>
        <p class="menu-item-description">{{ item.description }}</p>
        
        <button onclick="cart.addToCart({
            id: {{ item.id }},
            name: '{{ item.name }}',
            price: {{ item.price }},
            description: '{{ item.description|escapejs }}'
        }, 1)" class="btn btn-add-to-cart">
            🛒 Add to Cart
        </button>
    </div>
{% endfor %}

<style>
    .menu-item {
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
    }
    
    .menu-item-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .price {
        font-size: 18px;
        font-weight: 700;
        color: #f34949;
    }
    
    .menu-item-description {
        font-size: 13px;
        color: #666;
        margin-bottom: 12px;
    }
    
    .btn-add-to-cart {
        width: 100%;
        padding: 10px;
        background: linear-gradient(135deg, #f34949 0%, #d63d3d 100%);
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .btn-add-to-cart:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(243, 73, 73, 0.3);
    }
</style>
```

---

## Testing Integration

### Manual Test Steps

1. **Test Cart Button in Navbar**
   ```
   1. Go to home page
   2. Click "🛒 Cart" button in navbar
   3. Verify modal opens (should be empty)
   4. Close modal
   ```

2. **Test Add to Cart from Menu**
   ```
   1. Go to menu page
   2. Click "🛒 Add to Cart" on any item
   3. Verify toast notification appears
   4. Click cart button to verify item is there
   5. Try adding same item again - qty should update
   ```

3. **Test Checkout Flow**
   ```
   1. Add 2-3 items to cart
   2. Click "🛍️ Checkout" button or "Proceed to Checkout" in cart modal
   3. Verify redirect to /checkout/
   4. Verify page shows cart summary
   5. Click "Start Checkout"
   6. Verify first modal (Order Type) appears
   7. Complete all 4 steps
   8. Verify confirmation page
   ```

4. **Test Cart Persistence**
   ```
   1. Add items to cart
   2. Refresh page (F5)
   3. Verify cart still has items (localStorage)
   4. Close browser completely
   5. Reopen and go back to menu
   6. Verify cart still has items
   ```

### Automated Tests (Optional)
```javascript
// Test cart functionality in console
cart.addToCart({id: 1, name: 'Test', price: 10}, 2)
cart.getTotal()  // Should return subtotal with 21% tax
cart.getItemCount()  // Should return 2
cart.removeFromCart(1)
cart.getItemCount()  // Should return 0
```

---

## File Locations Summary

| Component | File | Status |
|-----------|------|--------|
| Cart JavaScript | `static/js/cart-system.js` | ✅ Created |
| Cart Modal | `templates/cart/cart_modal.html` | ✅ Created |
| Checkout Page | `templates/checkout/checkout.html` | ✅ Created |
| Order Type Modal | `templates/checkout/order_type_modal.html` | ✅ Created |
| Customer Modal | `templates/checkout/customer_details_modal.html` | ✅ Created |
| Review Modal | `templates/checkout/order_review_modal.html` | ✅ Created |
| Confirmation Page | `templates/checkout/confirmation.html` | ✅ Created |
| API Endpoints | `restaurant/api.py` | ✅ Created |
| Checkout Views | `restaurant/checkout_views.py` | ✅ Created |
| **BASE.HTML** | `templates/base.html` | ⏳ **NEEDS UPDATE** |
| **MENU.HTML** | `templates/restaurant/menu.html` | ⏳ **NEEDS UPDATE** |

---

## What's Ready vs. What's Needed

### ✅ Already Implemented
- Shopping cart system (JavaScript)
- Cart modal UI
- 4-step checkout flow
- All checkout modals
- Confirmation page
- API endpoints
- Django views and URL routing
- Database models (from Phase 1-2)
- Admin interface (from Phase 1-2)

### ⏳ Integration Needed
- Update base.html with cart script and navbar buttons
- Update menu.html with "Add to Cart" buttons
- Optional: Add styling to match your design

### ❌ Not Yet Implemented (Future Phases)
- Payment processing (Phase 4)
- Email notifications (Phase 4)
- Authentication backend (Phase 4)
- Order tracking real-time (Phase 5)
- Admin dashboard (Phase 6)

---

## Quick Integration Timeline

| Task | Time | Difficulty |
|------|------|-----------|
| Add script to base.html | 2 min | ⭐ Easy |
| Add navbar buttons | 5 min | ⭐ Easy |
| Update menu template | 10 min | ⭐ Easy |
| Test full flow | 10 min | ⭐ Easy |
| Fix styling issues | 15 min | ⭐⭐ Medium |
| **Total** | **~42 min** | - |

---

**Next Step**: Update base.html and menu.html with the code snippets above, then test the full flow!

