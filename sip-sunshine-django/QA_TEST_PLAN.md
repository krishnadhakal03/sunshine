# PHASE 3 QA/QC - COMPREHENSIVE TEST PLAN

**Date**: December 28, 2025  
**Test Lead**: Senior QA/QC  
**Project**: Sip Sunshine Django - Phase 3 Checkout System  
**Status**: 🔄 IN PROGRESS  

---

## 📋 TEST PLAN OVERVIEW

### Test Scope
- ✅ Unit Testing (APIs, Models, JavaScript)
- ✅ Smoke Testing (Basic functionality)
- ✅ Integration Testing (Component interactions)
- ✅ Flow Testing (End-to-end user journeys)
- ✅ Regression Testing (Existing functionality)

### Test Environment
- **Framework**: Django 4.2.7
- **Database**: PostgreSQL/MySQL (Django ORM)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Browser**: Chrome, Firefox, Safari, Edge

### Test Duration
- **Unit Tests**: 2-3 hours
- **Smoke Tests**: 1-2 hours
- **Integration Tests**: 2-3 hours
- **Flow Tests**: 2-3 hours
- **Regression Tests**: 1-2 hours
- **Total**: ~10-15 hours

---

## 1️⃣ UNIT TESTING

### 1.1 API ENDPOINT TESTING

#### Test Case 1.1.1: GET /api/settings/delivery/

**Description**: Test delivery settings API endpoint

**Prerequisites**: DeliverySettings record exists in database

**Test Steps**:
```
1. Send GET request to /api/settings/delivery/
2. Verify response status code = 200
3. Verify response is JSON
4. Verify response contains required fields:
   - delivery_enabled (boolean)
   - pickup_enabled (boolean)
   - delivery_charge_fixed (decimal)
   - delivery_charge_percentage (decimal)
   - estimated_pickup_time (integer)
   - estimated_delivery_time (integer)
   - minimum_order_amount (decimal)
   - service_radius_km (decimal)
5. Verify field values are correct types
6. Verify values are reasonable (charge > 0, time > 0)
```

**Expected Results**:
```json
{
  "delivery_enabled": true,
  "pickup_enabled": true,
  "delivery_charge_fixed": 2.50,
  "delivery_charge_percentage": 0.0,
  "estimated_pickup_time": 15,
  "estimated_delivery_time": 45,
  "minimum_order_amount": 10.00,
  "service_radius_km": 10.0
}
```

**Status**: ⏳ TO TEST

---

#### Test Case 1.1.2: GET /api/settings/delivery/ (No Settings)

**Description**: Test API when no DeliverySettings exist

**Prerequisites**: DeliverySettings deleted from database

**Test Steps**:
```
1. Delete all DeliverySettings records
2. Send GET request to /api/settings/delivery/
3. Verify response status code = 200
4. Verify default values returned
5. Verify response is valid JSON
```

**Expected Results**: Returns default settings (no error)

**Status**: ⏳ TO TEST

---

#### Test Case 1.1.3: POST /api/orders/create/ - Valid Dine-In Order

**Description**: Test creating a valid dine-in order

**Test Data**:
```json
{
  "order_type": "seated",
  "payment_method": "cash",
  "guest_name": "Test User",
  "guest_phone": "+31612345678",
  "guest_email": "test@example.com",
  "table_number": 5,
  "special_requests": "No onions",
  "items": [
    {
      "id": 1,
      "name": "Burger",
      "price": 12.50,
      "quantity": 2,
      "special_instructions": "Extra cheese"
    }
  ]
}
```

**Test Steps**:
```
1. Send POST request with valid data
2. Verify response status = 200
3. Verify success = true
4. Verify order_id returned
5. Verify order_number returned
6. Check database for Order record
7. Verify Order fields populated correctly
8. Check OrderItem records created
9. Verify totals calculated (subtotal, tax, total)
10. Verify payment_status = 'unpaid'
```

**Expected Results**:
- Order created successfully
- Order ID and number returned
- Database contains order and items
- Totals calculated correctly (subtotal + 21% tax)

**Status**: ⏳ TO TEST

---

#### Test Case 1.1.4: POST /api/orders/create/ - Valid Delivery Order

**Description**: Test creating a valid delivery order with address

**Test Data**:
```json
{
  "order_type": "delivery",
  "payment_method": "stripe",
  "guest_name": "Jane Doe",
  "guest_phone": "+31687654321",
  "guest_email": "jane@example.com",
  "delivery_address": "123 Main Street",
  "delivery_city": "Amsterdam",
  "delivery_postal_code": "1012AB",
  "delivery_instructions": "Ring doorbell",
  "items": [
    {
      "id": 1,
      "name": "Fries",
      "price": 5.00,
      "quantity": 1
    }
  ]
}
```

**Test Steps**:
```
1. Send POST with delivery order
2. Verify response status = 200
3. Verify success = true
4. Check database:
   - Order.order_type = 'delivery'
   - Order.delivery_charge > 0
   - Order.delivery_address populated
   - Order.delivery_city populated
   - Order.delivery_postal_code populated
5. Verify total = subtotal + tax + delivery_charge
```

**Expected Results**:
- Delivery order created
- Delivery charge included in total
- Address fields populated

**Status**: ⏳ TO TEST

---

#### Test Case 1.1.5: POST /api/orders/create/ - Valid Pickup Order

**Description**: Test creating a valid pickup order

**Test Data**:
```json
{
  "order_type": "pickup",
  "payment_method": "paypal",
  "guest_name": "John Smith",
  "guest_phone": "+31611111111",
  "preferred_pickup_time": "2024-01-15T14:30",
  "items": [
    {"id": 1, "name": "Pizza", "price": 15.00, "quantity": 1},
    {"id": 2, "name": "Salad", "price": 8.00, "quantity": 1}
  ]
}
```

**Test Steps**:
```
1. Send POST with pickup order
2. Verify response status = 200
3. Check Order fields:
   - order_type = 'pickup'
   - preferred_pickup_time set
   - delivery_charge = 0 (no delivery charge)
4. Verify subtotal = 23.00
5. Verify tax = 4.83 (21% of 23)
6. Verify total = 27.83
```

**Expected Results**:
- Pickup order created
- No delivery charge
- Pickup time saved
- Totals correct

**Status**: ⏳ TO TEST

---

#### Test Case 1.1.6: POST /api/orders/create/ - Missing Required Fields

**Description**: Test error handling for missing required fields

**Test Scenarios**:
```
a) Missing order_type
b) Missing payment_method
c) Missing guest_name
d) Missing guest_phone
e) Missing items array
f) Empty items array
g) Missing delivery address (for delivery order)
h) Missing table_number (for seated order)
```

**Test Steps** (for each scenario):
```
1. Send POST with missing field
2. Verify response status = 400
3. Verify success = false
4. Verify error message indicates missing field
5. Verify no order created in database
```

**Expected Results**:
- 400 error with descriptive message
- No database changes

**Status**: ⏳ TO TEST

---

#### Test Case 1.1.7: POST /api/orders/create/ - Invalid Order Type

**Description**: Test error handling for invalid order type

**Test Data**: `order_type: "invalid_type"`

**Test Steps**:
```
1. Send POST with invalid order_type
2. Verify response status = 400
3. Verify error message mentions valid types
```

**Expected Results**: 400 error, no order created

**Status**: ⏳ TO TEST

---

#### Test Case 1.1.8: POST /api/orders/create/ - Invalid Payment Method

**Description**: Test error handling for invalid payment method

**Test Data**: `payment_method: "bitcoin"`

**Test Steps**:
```
1. Send POST with invalid payment_method
2. Verify response status = 400
3. Verify error indicates valid methods
```

**Expected Results**: 400 error, no order created

**Status**: ⏳ TO TEST

---

#### Test Case 1.1.9: GET /api/orders/{id}/ - Valid Order

**Description**: Test retrieving order status

**Test Steps**:
```
1. Create an order (using POST /api/orders/create/)
2. Get order_id from response
3. Send GET /api/orders/{order_id}/
4. Verify response status = 200
5. Verify response contains:
   - id
   - order_number
   - status
   - order_type
   - guest_name
   - guest_phone
   - subtotal, tax, total_amount
   - payment_status
   - items array
6. Verify totals match order created
```

**Expected Results**: Order details returned correctly

**Status**: ⏳ TO TEST

---

#### Test Case 1.1.10: GET /api/orders/{id}/ - Invalid Order ID

**Description**: Test error handling for non-existent order

**Test Steps**:
```
1. Send GET /api/orders/99999/
2. Verify response status = 404
3. Verify error message
```

**Expected Results**: 404 error

**Status**: ⏳ TO TEST

---

### 1.2 MODEL TESTING

#### Test Case 1.2.1: Order Model - Calculation Methods

**Description**: Test Order model methods

**Test Cases**:
```python
1. order.calculate_total() returns correct value
2. order.is_paid() returns correct boolean
3. order.can_be_delivered() checks delivery status
```

**Test Steps**:
```
1. Create Order with known values
2. Call calculate_total()
3. Verify result = subtotal + tax + delivery_charge
4. Call is_paid() with payment_status='paid'
5. Verify returns True
6. Call is_paid() with payment_status='unpaid'
7. Verify returns False
```

**Expected Results**: Methods return correct values

**Status**: ⏳ TO TEST

---

#### Test Case 1.2.2: Cart Model - Add/Remove Operations

**Description**: Test Cart model CRUD operations

**Test Steps**:
```python
# Test add_item
cart = Cart.objects.create(session_key='test123')
cart.add_item({'id': 1, 'name': 'Burger', 'price': 12.50, 'quantity': 1})
assert cart.items contains burger

# Test remove_item
cart.remove_item(1)
assert cart.items is empty

# Test get_total
cart.add_item({'id': 1, 'name': 'Burger', 'price': 10.00, 'quantity': 2})
total = cart.get_total()
assert total = 10 * 2 * 1.21 = 24.20
```

**Expected Results**: All operations work correctly

**Status**: ⏳ TO TEST

---

#### Test Case 1.2.3: DeliverySettings - Delivery Charge Calculation

**Description**: Test delivery charge calculation

**Test Steps**:
```python
settings = DeliverySettings.objects.first()
settings.delivery_charge_fixed = 2.50
settings.delivery_charge_percentage = 5.0

# Test fixed only
charge = settings.calculate_delivery_charge(Decimal('100.00'))
assert charge = 2.50 (no percentage)

# Test with percentage
charge = settings.calculate_delivery_charge(Decimal('100.00'))
assert charge = 2.50 + (100 * 0.05) = 7.50
```

**Expected Results**: Correct charge calculation

**Status**: ⏳ TO TEST

---

### 1.3 JAVASCRIPT FUNCTION TESTING

#### Test Case 1.3.1: cart.addToCart() - New Item

**Test in Browser Console**:
```javascript
// Test data
const item = {id: 1, name: 'Burger', price: 12.50, description: 'Tasty burger'};

// Execute
cart.addToCart(item, 2);

// Verify
localStorage.sip_sunshine_cart  // Should contain item with qty 2
cart.getItemCount()  // Should return 2
```

**Expected Results**: Item added with correct quantity

**Status**: ⏳ TO TEST

---

#### Test Case 1.3.2: cart.addToCart() - Existing Item (Update Quantity)

**Test in Browser Console**:
```javascript
// Add first time
cart.addToCart({id: 1, name: 'Burger', price: 12.50}, 1);

// Add same item again
cart.addToCart({id: 1, name: 'Burger', price: 12.50}, 2);

// Verify
cart.getItemCount()  // Should return 3 (1 + 2)
// Check localStorage - should have ONE burger with qty 3
```

**Expected Results**: Quantity updated, not duplicate item added

**Status**: ⏳ TO TEST

---

#### Test Case 1.3.3: cart.removeFromCart() - Remove Item

**Test Steps**:
```javascript
cart.addToCart({id: 1, name: 'Burger', price: 12.50}, 2);
cart.removeFromCart(1);
cart.getItemCount()  // Should return 0
```

**Expected Results**: Item removed completely

**Status**: ⏳ TO TEST

---

#### Test Case 1.3.4: cart.updateQuantity() - Update to Valid Number

**Test Steps**:
```javascript
cart.addToCart({id: 1, name: 'Burger', price: 12.50}, 2);
cart.updateQuantity(1, 5);
cart.getItemCount()  // Should return 5
```

**Expected Results**: Quantity updated

**Status**: ⏳ TO TEST

---

#### Test Case 1.3.5: cart.updateQuantity() - Update to Zero (Remove)

**Test Steps**:
```javascript
cart.addToCart({id: 1, name: 'Burger', price: 12.50}, 2);
cart.updateQuantity(1, 0);
cart.getItemCount()  // Should return 0
// Item should be removed from cart
```

**Expected Results**: Item removed when qty set to 0

**Status**: ⏳ TO TEST

---

#### Test Case 1.3.6: cart.getTotal() - Correct Calculation with VAT

**Test Steps**:
```javascript
// Clear cart
cart.clearCart();

// Add items
cart.addToCart({id: 1, name: 'Burger', price: 10.00}, 1);
cart.addToCart({id: 2, name: 'Fries', price: 5.00}, 2);

// Calculate
// Subtotal = 10 + (5 * 2) = 20.00
// Tax (21%) = 4.20
// Total = 24.20

total = cart.getTotal();
assert total == 24.20
```

**Expected Results**: Total correctly includes 21% VAT

**Status**: ⏳ TO TEST

---

#### Test Case 1.3.7: cart localStorage Persistence

**Test Steps**:
```javascript
// Add items
cart.addToCart({id: 1, name: 'Burger', price: 12.50}, 2);

// Refresh page
location.reload();

// Verify
cart.getItemCount()  // Should still be 2
// Burger should still be in cart
```

**Expected Results**: Cart persists after page reload

**Status**: ⏳ TO TEST

---

---

## 2️⃣ SMOKE TESTING

### Test Case 2.1: Cart Page Loads

**Steps**:
```
1. Go to /menu/
2. Verify page loads successfully
3. Verify cart icon appears in navbar
4. Verify cart badge shows 0
```

**Expected**: Page loads, cart icon visible, no errors

**Status**: ⏳ TO TEST

---

### Test Case 2.2: Add to Cart Button Works

**Steps**:
```
1. Go to /menu/
2. Click "Add to Cart" button on any item
3. Verify toast notification appears
4. Verify cart badge increments
5. Click cart icon
6. Verify cart modal opens
7. Verify item displayed in cart
```

**Expected**: Item added, modal shows item

**Status**: ⏳ TO TEST

---

### Test Case 2.3: Checkout Page Loads

**Steps**:
```
1. Go to /checkout/
2. Verify page loads
3. Verify 4-step progress indicator visible
4. Verify "Start Checkout" button present
5. Verify cart summary displayed
```

**Expected**: Page loads with all elements

**Status**: ⏳ TO TEST

---

### Test Case 2.4: Order Type Modal Opens

**Steps**:
```
1. Go to /checkout/
2. Click "Start Checkout"
3. Verify order type modal appears
4. Verify 3 cards visible (Dine-In, Pickup, Delivery)
5. Verify each card has proper info
```

**Expected**: Modal displays correctly

**Status**: ⏳ TO TEST

---

### Test Case 2.5: Customer Details Modal Appears After Order Type

**Steps**:
```
1. From order type modal
2. Click any order type card
3. Verify modal closes
4. Verify customer details modal appears
5. Verify form fields displayed
```

**Expected**: Correct modal transition

**Status**: ⏳ TO TEST

---

### Test Case 2.6: Order Review Modal Shows After Customer Details

**Steps**:
```
1. Fill customer form
2. Click "Proceed"
3. Verify modal closes
4. Verify review modal appears
5. Verify order items listed
6. Verify totals displayed
```

**Expected**: Order summary visible

**Status**: ⏳ TO TEST

---

### Test Case 2.7: Order Can Be Submitted

**Steps**:
```
1. Complete review modal
2. Check terms checkbox
3. Click "Place Order"
4. Verify processing message appears
5. Verify redirect to confirmation page
```

**Expected**: Order submitted, confirmation page loads

**Status**: ⏳ TO TEST

---

### Test Case 2.8: Confirmation Page Displays

**Steps**:
```
1. After order submission
2. Verify confirmation page loads
3. Verify order number displayed
4. Verify status timeline shown
5. Verify tracking link present
```

**Expected**: Confirmation page complete

**Status**: ⏳ TO TEST

---

---

## 3️⃣ INTEGRATION TESTING

### Test Case 3.1: Cart → Checkout Page Integration

**Steps**:
```
1. Add items to cart
2. Click "Proceed to Checkout" in cart modal
3. Verify redirect to /checkout/
4. Verify cart items display in page
5. Verify sessionStorage updated with cart data
```

**Expected**: Cart data flows to checkout page

**Status**: ⏳ TO TEST

---

### Test Case 3.2: API Integration - Delivery Settings

**Steps**:
```
1. Go to /checkout/
2. Click "Start Checkout"
3. Order type modal loads
4. Verify API call to /api/settings/delivery/ made
5. Verify delivery times/charges displayed correctly
6. Check Network tab for API response
```

**Expected**: API called, settings displayed

**Status**: ⏳ TO TEST

---

### Test Case 3.3: Order Creation - API to Database

**Steps**:
```
1. Complete full checkout flow
2. Submit order
3. Verify API call to POST /api/orders/create/
4. Check response contains order_id
5. Go to Django admin
6. Verify Order record created with correct data
7. Verify OrderItem records created
8. Verify totals match frontend calculation
```

**Expected**: Order and items in database

**Status**: ⏳ TO TEST

---

### Test Case 3.4: Admin Interface Integration

**Steps**:
```
1. Go to Django admin
2. Navigate to Orders
3. Verify orders from checkout visible
4. Click order to view details
5. Verify all fields displayed correctly
6. Verify order status can be updated
```

**Expected**: Admin interface functional

**Status**: ⏳ TO TEST

---

### Test Case 3.5: sessionStorage Data Flow

**Steps**:
```
1. Open DevTools → Application → Session Storage
2. Start checkout
3. Select order type
4. Verify checkout_order_type set
5. Fill customer details
6. Verify checkout_customer_data set
7. Go to review
8. Verify data used in summary
```

**Expected**: Data persists through modals

**Status**: ⏳ TO TEST

---

---

## 4️⃣ FLOW TESTING

### Test Case 4.1: Complete Seated Dine-In Flow

**Steps**:
```
1. Go to /menu/
2. Add Burger (qty 2) to cart
3. Add Fries (qty 1) to cart
4. Click "Checkout"
5. Start checkout
6. Select "Dine-In"
7. Fill: Name, Phone, Table #5
8. Select "Cash" payment
9. Agree to terms
10. Submit order
11. Verify confirmation page
12. Check order in admin
```

**Verify**:
- ✓ Order created in database
- ✓ Order type = seated
- ✓ Table number = 5
- ✓ Items listed correctly
- ✓ Totals: Burger €25 + Fries €5 = €30 + €6.30 tax = €36.30
- ✓ Payment method = cash
- ✓ Payment status = unpaid (for cash)

**Status**: ⏳ TO TEST

---

### Test Case 4.2: Complete Pickup Flow

**Steps**:
```
1. Go to /menu/
2. Add item to cart
3. Go to /checkout/
4. Start checkout
5. Select "Pickup"
6. Fill: Name, Phone, Time 14:30
7. Select "Stripe" payment
8. Agree to terms
9. Submit order
10. Verify confirmation
```

**Verify**:
- ✓ Order created
- ✓ Order type = pickup
- ✓ No delivery charge in total
- ✓ Pickup time saved
- ✓ Status = pending

**Status**: ⏳ TO TEST

---

### Test Case 4.3: Complete Delivery Flow

**Steps**:
```
1. Add items to cart
2. Go to /checkout/
3. Start checkout
4. Select "Delivery"
5. Fill: Name, Phone, Full Address, City, Postal Code
6. Add: Delivery Instructions
7. Select "PayPal" payment
8. Agree to terms
9. Submit
10. Verify confirmation
```

**Verify**:
- ✓ Order created
- ✓ Order type = delivery
- ✓ Delivery charge included (€2.50)
- ✓ Total = subtotal + tax + delivery
- ✓ Address fields saved
- ✓ Instructions saved

**Status**: ⏳ TO TEST

---

### Test Case 4.4: Flow with Back Navigation

**Steps**:
```
1. Start checkout
2. Select order type (pickup)
3. Fill customer details
4. Click "Back" button
5. Verify returned to order type modal
6. Select different type (delivery)
7. Fill new address details
8. Continue to review
9. Verify delivery address shown (not pickup)
10. Submit order
```

**Verify**:
- ✓ Back button works
- ✓ Data can be changed
- ✓ Correct data used in order

**Status**: ⏳ TO TEST

---

### Test Case 4.5: Flow with Form Validation Errors

**Steps**:
```
1. Start checkout
2. Select order type
3. Try to proceed WITHOUT filling name
4. Verify error message appears
5. Fill required fields
6. Proceed successfully
```

**Verify**:
- ✓ Validation catches empty fields
- ✓ Error message clear
- ✓ User can fix and retry

**Status**: ⏳ TO TEST

---

### Test Case 4.6: Multi-Item Order Flow

**Steps**:
```
1. Add 5 different items to cart
2. Adjust quantities (various amounts)
3. Go to checkout
4. Complete dine-in order
5. Verify all items in confirmation
6. Check order in admin
```

**Verify**:
- ✓ All items in OrderItem table
- ✓ Quantities correct
- ✓ Total calculation correct

**Status**: ⏳ TO TEST

---

---

## 5️⃣ REGRESSION TESTING

### Test Case 5.1: Menu Page Still Works

**Steps**:
```
1. Go to /menu/
2. Verify page loads
3. Verify items display
4. Verify items have prices
5. Verify categories (if any)
6. Verify no broken links
```

**Expected**: Menu page unaffected

**Status**: ⏳ TO TEST

---

### Test Case 5.2: Admin Interface Still Works

**Steps**:
```
1. Go to /admin/
2. Verify login works
3. Navigate to existing models:
   - Pages
   - Blog posts
   - Menu items
   - Reservations
4. Verify CRUD operations work
```

**Expected**: Admin fully functional

**Status**: ⏳ TO TEST

---

### Test Case 5.3: Existing Views Still Work

**Steps**:
```
1. /home/ - loads
2. /about/ - loads
3. /blog/ - loads
4. /contact/ - loads
5. /reservation/ - loads
```

**Expected**: All pages accessible

**Status**: ⏳ TO TEST

---

### Test Case 5.4: No JavaScript Errors

**Steps**:
```
1. Go to /menu/
2. Open DevTools → Console
3. Verify no errors shown
4. Go to /checkout/
5. Verify no errors
6. Complete checkout flow
7. Check console throughout
```

**Expected**: No error messages

**Status**: ⏳ TO TEST

---

### Test Case 5.5: Database Integrity

**Steps**:
```
1. Check all new models have proper relationships
2. Verify Order → OrderItem relationship
3. Verify Order → User relationship (nullable)
4. Check no orphaned records
5. Verify indexes exist
```

**Expected**: Database structure intact

**Status**: ⏳ TO TEST

---

---

## 📊 TEST RESULTS SUMMARY

| Test Category | Total Tests | Passed | Failed | Blocked |
|---------------|-------------|--------|--------|---------|
| Unit Testing - API | 10 | 0 | 0 | 0 |
| Unit Testing - Models | 3 | 0 | 0 | 0 |
| Unit Testing - JS | 7 | 0 | 0 | 0 |
| Smoke Testing | 8 | 0 | 0 | 0 |
| Integration Testing | 5 | 0 | 0 | 0 |
| Flow Testing | 6 | 0 | 0 | 0 |
| Regression Testing | 5 | 0 | 0 | 0 |
| **TOTAL** | **44** | **0** | **0** | **0** |

---

## 🐛 ISSUES FOUND

*To be filled after testing*

---

## ✅ TEST EXECUTION SCHEDULE

- **Phase 1**: Unit Testing (API) - 3 hours
- **Phase 2**: Unit Testing (Models + JS) - 2 hours
- **Phase 3**: Smoke Testing - 2 hours
- **Phase 4**: Integration Testing - 3 hours
- **Phase 5**: Flow Testing - 3 hours
- **Phase 6**: Regression Testing - 2 hours
- **Phase 7**: Bug Fixing & Re-testing - 2 hours

---

**Test Lead**: Senior QA/QC  
**Date Started**: December 28, 2025  
**Status**: 🔄 IN PROGRESS

