# PHASE 3 QA/QC TESTING GUIDE
## Complete Testing Execution Handbook

**Document Version:** 1.0  
**Date Created:** 2024-01-15  
**Audience:** QA Engineers, Developers, Testers  
**Purpose:** Complete guide for executing Phase 3 comprehensive testing

---

## 📑 TABLE OF CONTENTS

1. [Quick Start](#quick-start)
2. [Test Infrastructure](#test-infrastructure)
3. [Unit Tests](#unit-tests)
4. [Smoke Tests](#smoke-tests)
5. [Integration Tests](#integration-tests)
6. [Flow Tests](#flow-tests)
7. [Regression Tests](#regression-tests)
8. [Manual Testing](#manual-testing)
9. [Bug Tracking](#bug-tracking)
10. [Test Report](#test-report)

---

## 🚀 QUICK START

### 5-Minute Setup

```bash
# 1. Navigate to project root
cd /path/to/sip-sunshine-django

# 2. Run all automated tests
pytest tests/test_phase3_*.py -v --tb=short

# 3. View results
# Check pass/fail counts
# Review any failures
```

### Command Reference

```bash
# Run all tests
pytest tests/test_phase3_*.py -v

# Run specific test class
pytest tests/test_phase3_unit.py::APIDeliverySettingsTest -v

# Run specific test method
pytest tests/test_phase3_unit.py::APIDeliverySettingsTest::test_delivery_settings_returns_200 -v

# Run with coverage
pytest tests/test_phase3_*.py --cov=restaurant --cov-report=html

# Run master test runner
python run_all_tests.py

# Run and generate HTML report
pytest tests/test_phase3_*.py -v --html=report.html --self-contained-html
```

---

## 🏗️ TEST INFRASTRUCTURE

### File Structure

```
sip-sunshine-django/
├── tests/
│   ├── __init__.py
│   ├── test_phase3_unit.py          (20+ unit tests)
│   ├── test_phase3_integration.py   (20+ integration/flow tests)
│   └── test_phase3_smoke_regression.py  (25+ smoke/regression tests)
├── run_all_tests.py                  (Master test runner)
├── QA_TEST_PLAN.md                   (Test plan document)
├── QA_TEST_EXECUTION_REPORT.md      (Execution results)
└── QA_TESTING_GUIDE.md              (This file)
```

### Test Framework Setup

```python
# Framework: Django TestCase + pytest
# Test Runner: pytest
# Coverage: coverage.py (optional)

# Install dependencies
pip install pytest pytest-django pytest-cov
```

### Configuration

```ini
# pytest.ini or setup.cfg
[pytest]
DJANGO_SETTINGS_MODULE = sip_sunshine.settings
python_files = test_*.py
testpaths = tests
```

---

## 🧪 UNIT TESTS

### What Are Unit Tests?

Tests that verify individual components work correctly in isolation:
- API endpoints (request → response)
- Model methods (input → output)
- Database operations (create, read, update)

### Unit Test Files

**File:** `tests/test_phase3_unit.py`  
**Tests:** 20+ individual test methods  
**Duration:** ~15 minutes  
**Dependencies:** Django models, settings

### Test Classes

#### 1️⃣ APIDeliverySettingsTest (5 tests)

```python
# Tests GET /api/settings/delivery/

Test 1.1: test_delivery_settings_returns_200
Purpose: Verify endpoint returns HTTP 200
Command: pytest tests/test_phase3_unit.py::APIDeliverySettingsTest::test_delivery_settings_returns_200 -v
Expected: Response status = 200

Test 1.2: test_delivery_settings_returns_json
Purpose: Verify response is valid JSON
Command: pytest tests/test_phase3_unit.py::APIDeliverySettingsTest::test_delivery_settings_returns_json -v
Expected: JSON parse succeeds, no errors

Test 1.3: test_delivery_settings_contains_required_fields
Purpose: Verify all required fields present
Command: pytest tests/test_phase3_unit.py::APIDeliverySettingsTest::test_delivery_settings_contains_required_fields -v
Expected: Response contains delivery_charge_fixed, estimated_delivery_time

Test 1.4: test_delivery_settings_correct_values
Purpose: Verify field values correct
Command: pytest tests/test_phase3_unit.py::APIDeliverySettingsTest::test_delivery_settings_correct_values -v
Expected: delivery_charge_fixed = 2.50, estimated_delivery_time = 30

Test 1.5: test_delivery_settings_no_record_returns_defaults
Purpose: Verify defaults returned when no DB record
Command: pytest tests/test_phase3_unit.py::APIDeliverySettingsTest::test_delivery_settings_no_record_returns_defaults -v
Expected: API returns default values even with empty DB
```

#### 2️⃣ APICreateOrderTest (6 tests)

```python
# Tests POST /api/orders/create/

Test 2.1: test_create_valid_seated_order
Purpose: Verify seated order creation
Command: pytest tests/test_phase3_unit.py::APICreateOrderTest::test_create_valid_seated_order -v
Input: {order_type: 'seated', table_number: 5, items: [...]}
Expected: Order created, ID returned, database updated

Test 2.2: test_create_valid_pickup_order
Purpose: Verify pickup order creation
Command: pytest tests/test_phase3_unit.py::APICreateOrderTest::test_create_valid_pickup_order -v
Input: {order_type: 'pickup', items: [...]}
Expected: Order type = 'pickup', no delivery charge

Test 2.3: test_create_valid_delivery_order
Purpose: Verify delivery order creation with charge
Command: pytest tests/test_phase3_unit.py::APICreateOrderTest::test_create_valid_delivery_order -v
Input: {order_type: 'delivery', delivery_address: '...', items: [...]}
Expected: delivery_charge = 2.50, total includes charge

Test 2.4: test_create_order_missing_required_field
Purpose: Verify validation errors for missing fields
Command: pytest tests/test_phase3_unit.py::APICreateOrderTest::test_create_order_missing_required_field -v
Input: Missing table_number for seated order
Expected: Status 400, error message

Test 2.5: test_create_order_invalid_order_type
Purpose: Verify validation for invalid order type
Command: pytest tests/test_phase3_unit.py::APICreateOrderTest::test_create_order_invalid_order_type -v
Input: {order_type: 'invalid', ...}
Expected: Status 400, error message

Test 2.6: test_create_order_totals_calculation
Purpose: Verify math is correct
Command: pytest tests/test_phase3_unit.py::APICreateOrderTest::test_create_order_totals_calculation -v
Input: Items totaling $30.00
Expected: Tax = $6.30 (21%), Total = $36.30
```

#### 3️⃣ APIGetOrderTest (2 tests)

```python
# Tests GET /api/orders/{id}/

Test 3.1: test_get_order_valid_id
Purpose: Retrieve existing order
Command: pytest tests/test_phase3_unit.py::APIGetOrderTest::test_get_order_valid_id -v
Input: Valid order ID
Expected: Status 200, order data returned

Test 3.2: test_get_order_invalid_id
Purpose: Handle non-existent order
Command: pytest tests/test_phase3_unit.py::APIGetOrderTest::test_get_order_invalid_id -v
Input: Non-existent order ID
Expected: Status 404, not found
```

#### 4️⃣ OrderModelTest (3 tests)

```python
# Tests Order model

Test 4.1: test_order_creation
Purpose: Verify order model creates
Command: pytest tests/test_phase3_unit.py::OrderModelTest::test_order_creation -v
Expected: ID and order_number auto-generated

Test 4.2: test_order_string_representation
Purpose: Verify __str__ method
Command: pytest tests/test_phase3_unit.py::OrderModelTest::test_order_string_representation -v
Expected: __str__ returns meaningful string

Test 4.3: test_order_payment_status_calculation
Purpose: Verify is_paid() method
Command: pytest tests/test_phase3_unit.py::OrderModelTest::test_order_payment_status_calculation -v
Expected: Method returns correct boolean
```

#### 5️⃣ CartModelTest (3 tests)

```python
# Tests Cart model

Test 5.1: test_cart_creation
Purpose: Verify cart model creates
Command: pytest tests/test_phase3_unit.py::CartModelTest::test_cart_creation -v
Expected: Cart ID assigned

Test 5.2: test_cart_add_item
Purpose: Verify add_item() method
Command: pytest tests/test_phase3_unit.py::CartModelTest::test_cart_add_item -v
Expected: Item added to cart correctly

Test 5.3: test_cart_get_total
Purpose: Verify total calculation with VAT
Command: pytest tests/test_phase3_unit.py::CartModelTest::test_cart_get_total -v
Expected: Total = subtotal * 1.21
```

#### 6️⃣ DeliverySettingsModelTest (1 test)

```python
# Tests DeliverySettings model

Test 6.1: test_delivery_charge_calculation
Purpose: Verify charge = fixed + (amount * percentage)
Command: pytest tests/test_phase3_unit.py::DeliverySettingsModelTest::test_delivery_charge_calculation -v
Expected: Calculation correct
```

### Running Unit Tests

```bash
# Run all unit tests
pytest tests/test_phase3_unit.py -v

# Run all API tests
pytest tests/test_phase3_unit.py::API* -v

# Run all model tests
pytest tests/test_phase3_unit.py::*ModelTest -v

# Run with detailed output
pytest tests/test_phase3_unit.py -v -s

# Run with traceback
pytest tests/test_phase3_unit.py -v --tb=long
```

### Interpreting Results

```
PASSED (✓) - Test executed successfully, all assertions passed
FAILED (✗) - Test failed, assertion did not pass
ERROR (✗) - Test could not run due to error
SKIPPED (⊘) - Test was skipped

Example Output:
test_delivery_settings_returns_200 PASSED           [5%]
test_delivery_settings_returns_json PASSED          [10%]
test_delivery_settings_contains_required_fields PASSED [15%]
...
====== 20 passed in 15.23s ======
```

---

## 💨 SMOKE TESTS

### What Are Smoke Tests?

Quick tests that verify basic functionality works without deep testing:
- Pages load without 404
- Endpoints exist and respond
- Basic CRUD operations work
- No obvious errors

### File: `tests/test_phase3_smoke_regression.py`

**Classes:** SmokeTestCheckoutPage, SmokeTestOrderCreationAPI, SmokeTestDeliverySettings, SmokeTestOrderRetrieval  
**Tests:** 8 quick tests  
**Duration:** ~10 minutes

### Smoke Test Scenarios

```bash
# Run all smoke tests
pytest tests/test_phase3_smoke_regression.py::SmokeTest* -v

Test 1: Checkout page loads
- GET /checkout/ → 200
- Page contains "Secure Checkout" title

Test 2: Checkout page has modals
- Page includes orderTypeModal
- Page includes customerDetailsModal
- Page includes orderReviewModal

Test 3: API endpoints exist
- POST /api/orders/create/ → not 404
- GET /api/settings/delivery/ → not 404
- GET /api/orders/{id}/ → not 404

Test 4: APIs return JSON
- Valid JSON response format
- JSON can be parsed without errors

Test 5: APIs return required fields
- delivery_charge_fixed in response
- order_id in order creation response
```

### Running Smoke Tests

```bash
# Run all smoke tests
pytest tests/test_phase3_smoke_regression.py::SmokeTest* -v

# Run checkout page tests only
pytest tests/test_phase3_smoke_regression.py::SmokeTestCheckoutPage -v

# Run API tests only
pytest tests/test_phase3_smoke_regression.py::SmokeTestOrderCreationAPI -v
```

---

## 🔗 INTEGRATION TESTS

### What Are Integration Tests?

Tests that verify multiple components work together:
- API → Database flow
- Cart → Checkout integration
- Form submission → Database persistence

### File: `tests/test_phase3_integration.py`

**Classes:** CartCheckoutIntegrationTest, APIOrderCreationIntegrationTest, AdminIntegrationTest  
**Tests:** 5 integration tests  
**Duration:** ~20 minutes

### Integration Test Scenarios

```bash
# Run all integration tests
pytest tests/test_phase3_integration.py::*IntegrationTest -v

Test 1: Checkout page integration
- Checkout page loads successfully
- All required modals present on page

Test 2: Order creation with items
- Order created via API
- OrderItem records created for each item
- Items linked to order correctly

Test 3: Delivery order with charge
- Delivery order created
- delivery_charge = $2.50
- Total includes delivery charge
- Calculation: (subtotal * 1.21) + delivery_charge

Test 4: Seated order without charge
- Seated order created
- delivery_charge = $0.00
- Total = (subtotal * 1.21)

Test 5: Admin integration
- Order visible in admin
- Order data retrievable
```

### Running Integration Tests

```bash
# Run all integration tests
pytest tests/test_phase3_integration.py::*IntegrationTest -v

# Run cart checkout tests
pytest tests/test_phase3_integration.py::CartCheckoutIntegrationTest -v

# Run API creation tests
pytest tests/test_phase3_integration.py::APIOrderCreationIntegrationTest -v
```

---

## 🔄 FLOW TESTS

### What Are Flow Tests?

End-to-end tests that verify complete user workflows:
- User selects order type
- User enters details
- User reviews order
- Order is created

### File: `tests/test_phase3_integration.py`

**Classes:** SeatedDineInFlowTest, PickupOrderFlowTest, DeliveryOrderFlowTest, MultiItemOrderFlowTest, ValidationFlowTest  
**Tests:** 6 complete workflow tests  
**Duration:** ~45 minutes

### Flow Test Scenarios

#### Flow 1: Seated Dine-In Order
```
User: Customer dining in, paying with cash
Steps:
1. Select "Seated" order type
2. Enter table number: 5
3. Enter name: John Doe
4. Enter phone: +31612345678
5. Add 2 Burgers ($12.50 each) + 1 Fries ($5.00)
6. Review order (total should be $36.30)
7. Submit order
8. Receive confirmation

Expected:
✓ Order type = 'seated'
✓ Table number = 5
✓ Subtotal = $30.00
✓ Tax = $6.30
✓ Delivery charge = $0.00
✓ Total = $36.30
✓ Order status = 'pending'

Command: pytest tests/test_phase3_integration.py::SeatedDineInFlowTest::test_complete_seated_flow -v
```

#### Flow 2: Pickup Order
```
User: Customer ordering for pickup with Stripe
Steps:
1. Select "Pickup" order type
2. Enter name: Jane Smith
3. Enter phone: +31687654321
4. Select pickup time: 14:30 today
5. Add 2 Pizzas ($15.00 each)
6. Select Stripe payment
7. Complete payment
8. Receive confirmation

Expected:
✓ Order type = 'pickup'
✓ Pickup time stored
✓ Payment method = 'stripe'
✓ Delivery charge = $0.00
✓ Total = $36.30

Command: pytest tests/test_phase3_integration.py::PickupOrderFlowTest::test_complete_pickup_flow -v
```

#### Flow 3: Delivery Order
```
User: Customer ordering delivery
Steps:
1. Select "Delivery" order type
2. Enter name: Bob Johnson
3. Enter phone: +31611111111
4. Enter address: 456 Oak Avenue
5. Enter city: Rotterdam
6. Enter postal code: 3011AB
7. Enter special instructions: "Leave at door"
8. Add items, review, submit

Expected:
✓ Order type = 'delivery'
✓ Delivery address saved
✓ Postal code = '3011AB'
✓ Delivery charge = $2.50
✓ Total includes delivery charge

Command: pytest tests/test_phase3_integration.py::DeliveryOrderFlowTest::test_complete_delivery_flow -v
```

#### Flow 4: Multi-Item Order
```
User: Ordering 5 different items
Steps:
1. Select order type
2. Add 5 different items with varying quantities
3. Review total
4. Submit order

Expected:
✓ All 5 items in order
✓ Quantities preserved
✓ Subtotal correct
✓ Tax calculated
✓ Total correct

Command: pytest tests/test_phase3_integration.py::MultiItemOrderFlowTest::test_multi_item_order -v
```

#### Flow 5: Validation Error Handling
```
User: Submits incomplete form
Steps:
1. Start checkout
2. Attempt to submit without required fields
3. Receive error messages
4. Correct form
5. Resubmit successfully

Expected:
✓ Missing table_number rejected
✓ Missing address rejected
✓ Missing items rejected
✓ Error messages clear
✓ Can correct and retry

Command: pytest tests/test_phase3_integration.py::ValidationFlowTest -v
```

### Running Flow Tests

```bash
# Run all flow tests
pytest tests/test_phase3_integration.py::*FlowTest -v

# Run specific flow
pytest tests/test_phase3_integration.py::SeatedDineInFlowTest -v

# Run with detailed output
pytest tests/test_phase3_integration.py::*FlowTest -v -s
```

---

## 🔁 REGRESSION TESTS

### What Are Regression Tests?

Tests that verify existing features still work after changes:
- Menu page still loads
- Cart still functions
- Order types still work
- Payment methods still work

### File: `tests/test_phase3_smoke_regression.py`

**Classes:** RegressionTest*  
**Tests:** 25+ regression tests  
**Duration:** ~30 minutes

### Regression Test Categories

#### 1. Menu Functionality
```bash
pytest tests/test_phase3_smoke_regression.py::RegressionTestMenuPage -v

Tests:
✓ Menu page loads
✓ Menu items display
✓ Prices show correctly
```

#### 2. Cart Model
```bash
pytest tests/test_phase3_smoke_regression.py::RegressionTestCartModel -v

Tests:
✓ Cart creation works
✓ Can add items to cart
✓ Item quantities work correctly
```

#### 3. Order Model
```bash
pytest tests/test_phase3_smoke_regression.py::RegressionTestOrderModel -v

Tests:
✓ Order model creates records
✓ Order number auto-generated
✓ Status defaults to pending
✓ Payment status defaults to unpaid
```

#### 4. Order Types
```bash
pytest tests/test_phase3_smoke_regression.py::RegressionTestOrderTypes -v

Tests:
✓ Seated order type works
✓ Pickup order type works
✓ Delivery order type works
```

#### 5. Payment Methods
```bash
pytest tests/test_phase3_smoke_regression.py::RegressionTestPaymentMethods -v

Tests:
✓ Cash payment works
✓ Stripe payment works
✓ PayPal payment works
```

#### 6. Tax Calculation
```bash
pytest tests/test_phase3_smoke_regression.py::RegressionTestTaxCalculation -v

Tests:
✓ VAT = 21%
✓ Total includes tax
```

#### 7. Database Integrity
```bash
pytest tests/test_phase3_smoke_regression.py::RegressionTestDatabaseIntegrity -v

Tests:
✓ Guest name stored correctly
✓ Phone number stored correctly
✓ Order → OrderItem relationship works
```

### Running Regression Tests

```bash
# Run all regression tests
pytest tests/test_phase3_smoke_regression.py::Regression* -v

# Run specific regression category
pytest tests/test_phase3_smoke_regression.py::RegressionTestOrderModel -v

# Run all regression tests with coverage
pytest tests/test_phase3_smoke_regression.py::Regression* -v --cov=restaurant
```

---

## 🖱️ MANUAL TESTING

### Browser-Based Testing

Manual tests that require human interaction and visual verification.

### Setup

```bash
# 1. Start Django server
python manage.py runserver

# 2. Open in browser
http://localhost:8000/checkout/

# 3. Open browser console
# Windows/Linux: F12
# Mac: Cmd + Option + I
```

### JavaScript Function Testing

```javascript
// In browser console, test each function:

// Test 1: addToCart()
addToCart({name: 'Burger', price: 12.50, quantity: 1})
// Expected: Item added, console shows confirmation

// Test 2: removeFromCart()
removeFromCart(0)
// Expected: First item removed from cart

// Test 3: updateQuantity()
updateQuantity(0, 2)
// Expected: First item quantity set to 2

// Test 4: getTotal()
console.log(getTotal())
// Expected: Total price calculated correctly

// Test 5: localStorage persistence
// Refresh page, check cart is still there
// Expected: Cart items persist after refresh
```

### Checkout UI Testing

```
Test 1: Visual Verification
☐ Checkout page loads cleanly
☐ Header displays correctly
☐ Footer displays correctly
☐ No layout issues
☐ Colors look correct

Test 2: Modal Testing
☐ Order Type modal opens
☐ Customer Details modal opens
☐ Review modal opens
☐ All modals close correctly
☐ Modal transitions smooth
☐ Back buttons work

Test 3: Form Input
☐ Text fields accept input
☐ Phone field validates
☐ Email field validates
☐ Address field accepts long text
☐ Numbers in price fields

Test 4: Validation Messages
☐ Required field errors appear
☐ Error messages are clear
☐ Error styling is obvious
☐ Success messages appear
☐ Messages disappear after action

Test 5: Complete Checkout Flow
☐ Can select order type
☐ Can enter customer details
☐ Can review order
☐ Can submit order
☐ Confirmation page appears
✓ Order number displayed
```

### Testing Different Order Types

```
SEATED ORDER:
☐ Select "Seated" type
☐ Table number field appears
☐ Customer details fields appear
☐ Add items work
☐ Review shows no delivery charge
☐ Can submit

PICKUP ORDER:
☐ Select "Pickup" type
☐ Table number field hidden
☐ Pickup time field appears
☐ Delivery address field hidden
☐ Review shows no delivery charge
☐ Can submit

DELIVERY ORDER:
☐ Select "Delivery" type
☐ Address field appears
☐ City field appears
☐ Postal code field appears
☐ Review shows delivery charge
☐ Cannot submit without address
✓ Can submit with complete info
```

### Cross-Browser Testing

Test in multiple browsers:
```
✓ Chrome/Chromium
  - Latest version
  - Desktop view
  - Mobile view

✓ Firefox
  - Latest version
  - Desktop view
  - Mobile view

✓ Safari
  - Latest version
  - Desktop view
  - Mobile view
```

---

## 🐛 BUG TRACKING

### Bug Report Template

```
Bug ID: BUG-###
Title: [Brief description]
Severity: Critical | High | Medium | Low
Status: Open | In Progress | Fixed | Closed

Description:
[What is the bug?]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected Result:
[What should happen]

Actual Result:
[What actually happened]

Screenshots/Video:
[Attach if applicable]

Browser/OS:
[Chrome 121 on Windows 11, Firefox 121 on Mac, etc.]

Affected Test Case:
[Which test found it: TEST-###]
```

### Severity Levels

- **Critical**: System down, data loss, security issue
- **High**: Major feature broken, workaround exists
- **Medium**: Feature partially broken or has issues
- **Low**: Minor UI issue, cosmetic problem

### Known Issues

| ID | Title | Severity | Status |
|----|-------|----------|--------|
| - | [To be filled during testing] | - | - |

---

## 📊 TEST REPORT

### Test Execution Report Template

```
PHASE 3 TEST EXECUTION REPORT
Generated: [Date/Time]
Tester: [Name]
Environment: [Django 4.2.7, Python 3.10, PostgreSQL]

SUMMARY
Total Tests: [#]
Passed: [#] (XX%)
Failed: [#] (XX%)
Skipped: [#]
Duration: [#] hours

BY CATEGORY
Unit Tests: [#] passed, [#] failed
Smoke Tests: [#] passed, [#] failed
Integration Tests: [#] passed, [#] failed
Flow Tests: [#] passed, [#] failed
Regression Tests: [#] passed, [#] failed

ISSUES FOUND
[List any bugs found]

BLOCKERS
[Any issues preventing deployment]

RECOMMENDATIONS
[Deployment ready? What needs fixing?]

SIGN-OFF
Tester: _____ Date: _____
Tech Lead: _____ Date: _____
```

### Creating Report

```bash
# Generate automated report
pytest tests/test_phase3_*.py -v --html=report.html --self-contained-html

# View report
open report.html

# Or use master runner
python run_all_tests.py
```

---

## ✅ TESTING CHECKLIST

- [ ] All 20+ unit tests pass
- [ ] All 8 smoke tests pass
- [ ] All 5 integration tests pass
- [ ] All 6 flow tests pass
- [ ] All 25+ regression tests pass
- [ ] Manual browser testing completed
- [ ] All 3 order types verified
- [ ] All payment methods verified
- [ ] No JavaScript errors in console
- [ ] Checkout UI looks correct
- [ ] Validation errors work
- [ ] Success messages appear
- [ ] All modals work
- [ ] Complete checkout flow works
- [ ] Cross-browser testing done
- [ ] Test report generated
- [ ] No critical/high bugs
- [ ] Ready for deployment

---

## 🎯 SUCCESS CRITERIA

All tests pass = **✅ DEPLOYMENT READY**

```
✓ 100% of unit tests pass
✓ 100% of smoke tests pass
✓ 100% of integration tests pass
✓ 100% of flow tests pass
✓ 100% of regression tests pass
✓ Manual testing completed
✓ No critical issues
✓ No high-priority issues
```

---

**Document Version:** 1.0  
**Last Updated:** 2024-01-15  
**Next Review:** After test execution
