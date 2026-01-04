# Order Management System - Implementation Guide

## Overview
A complete order management system has been implemented for "Sip and Sunshine" restaurant to handle both **seated customers** and **online orders**.

---

## Architecture

### 1. **Database Models**

#### Order Model
```
- guest_name: CharField (required)
- guest_email: EmailField (optional)
- guest_phone: CharField (optional)
- order_type: Choice Field (seated/online)
- table_number: IntegerField (seated customers only)
- total_price: DecimalField (auto-calculated)
- status: Choice Field (pending/confirmed/preparing/ready/completed/cancelled)
- special_requests: TextField
- created_at: DateTime (auto-set)
- updated_at: DateTime (auto-updated)
- completed_at: DateTime (null until order completion)
```

#### OrderItem Model (Related to Order)
```
- order: ForeignKey to Order
- menu_item: ForeignKey to MenuItem (nullable)
- item_name: CharField (captured at order time)
- item_price: DecimalField (captured at order time)
- quantity: IntegerField (default: 1)
- special_instructions: TextField
- created_at: DateTime
```

### 2. **User Interface - Order Modal**

#### Features:
- **Order Type Selection**: Toggle between "Seated Customer" and "Online Order"
- **Conditional Fields**:
  - Seated: Shows table number field
  - Online: Shows email and phone fields
- **Item Display**: Shows selected item, price
- **Quantity Selector**: +/- buttons to adjust quantity
- **Guest Information**: Captures guest name (required for both types)
- **Special Instructions**: Text area for dietary needs, allergies, preferences

### 3. **Data Capture Flow**

#### For Seated Customers:
1. Guest clicks "Add to Order"
2. Modal opens with order type defaulting to "Seated"
3. Captures:
   - Guest name (required)
   - Table number (optional)
   - Item details (auto-populated)
   - Quantity
   - Special instructions
4. Staff can immediately fulfill order

#### For Online Orders:
1. Guest clicks "Add to Order"
2. Guest selects "Online Order" from toggle
3. Captures:
   - Guest name (required)
   - Email address (required)
   - Phone number (required)
   - Item details (auto-populated)
   - Quantity
   - Special instructions
4. System can send confirmation via email/SMS

### 4. **Order Creation Flow**

```
User clicks "Add to Order" button
    ↓
Order Modal opens with:
- Item name & price pre-filled
- Order type selector (Seated/Online)
- Quantity selector (default: 1)
- Guest information form
    ↓
User selects order type:
- If Seated: Show table number field
- If Online: Show email & phone fields
    ↓
User fills required fields:
- Guest name (always required)
- Table number OR (Email + Phone)
- Optional: Special instructions
    ↓
User clicks "Create Order"
    ↓
AJAX POST request to /orders/create/
    ↓
Server validates data
    ↓
Order created in database with:
- Order record with all details
- OrderItem record linking to menu item
- Total price calculated
- Status set to "pending"
    ↓
Success notification shows:
- Order #ID
- Guest name
- Item and quantity
```

### 5. **API Endpoint**

**URL**: `/orders/create/`
**Method**: POST
**Request Parameters**:
```
- guest_name: string (required)
- item_name: string (required)
- item_price: float (required)
- quantity: integer (default: 1)
- order_type: string ('seated' or 'online')
- special_instructions: string (optional)
- table_number: integer (required if order_type='seated')
- guest_email: string (required if order_type='online')
- guest_phone: string (required if order_type='online')
- csrfmiddlewaretoken: string (Django CSRF token)
```

**Response**:
```json
{
  "success": true,
  "order_id": 123,
  "message": "Order created successfully"
}
```

---

## Use Cases

### Use Case 1: Waiter Takes Order from Seated Customer
1. Customer browsing menu on tablet/screen at table
2. Customer clicks "Add to Order" for Pasta Carbonara
3. Modal opens:
   - Order Type: "Seated" (default)
   - Table Number: 5
   - Guest Name: "John Smith"
   - Item: "Pasta Carbonara" - $18.00
   - Quantity: 1
   - Special Instructions: "No bacon"
4. Waiter clicks "Create Order"
5. System creates order and assigns to kitchen
6. Kitchen receives order details including special instructions

### Use Case 2: Online Customer Ordering from Website
1. Customer browsing menu on website from home
2. Customer clicks "Add to Order" for House Special BBQ
3. Modal opens:
   - Order Type: Toggle to "Online Order"
   - Email Field: "customer@email.com"
   - Phone Field: "+32 123 456 789"
   - Guest Name: "Sarah Johnson"
   - Item: "House Special BBQ" - $25.00
   - Quantity: 2
   - Special Instructions: "Extra spicy, arrive at 19:00"
4. Customer clicks "Create Order"
5. System creates order with pending status
6. Email confirmation sent to customer
7. Order ready for pickup/delivery at specified time

### Use Case 3: Multiple Items Order (Future Enhancement)
```
Future: Allow adding multiple items to cart before checkout
- Add item 1 → Modal opens → Add to cart
- Add item 2 → Modal opens → Add to cart
- View cart → Review all items, quantities, total
- Checkout → Single order with multiple OrderItems
```

---

## Key Benefits

### For Restaurant Staff:
✅ Quickly capture table-based orders  
✅ See all special instructions  
✅ Track order status (pending→preparing→ready→completed)  
✅ Access order history by date, status, customer  

### For Online Customers:
✅ Easy self-service ordering from website  
✅ Capture preferences and allergies  
✅ Confirmation via email  
✅ Order tracking (if admin panel implemented)  

### For Management:
✅ Track revenue per order type (seated vs online)  
✅ Popular menu items by order frequency  
✅ Peak ordering times  
✅ Customer preferences and special requests patterns  

---

## Admin Interface Features

The Django admin includes:
1. **Order Management**:
   - Filter by status (pending, confirmed, preparing, ready, completed, cancelled)
   - Filter by order type (seated, online)
   - View guest details
   - Edit order status
   - View order items and prices

2. **Analytics Available**:
   - Total orders by type
   - Revenue by order type
   - Average order value
   - Most ordered items

---

## Future Enhancements

1. **Shopping Cart**: Allow multiple items before checkout
2. **Order Confirmation Emails**: Automated email to online customers
3. **SMS Notifications**: Notify customers when order is ready
4. **Payment Integration**: Add payment processing for online orders
5. **Table Management**: Track table availability and capacity
6. **Order Tracking Page**: Allow customers to track their online order status
7. **Staff Dashboard**: Real-time kitchen display with order queue
8. **Inventory Management**: Decrease stock when order created
9. **Analytics Dashboard**: Charts and reports on sales, top items, peak hours
10. **Multi-language Support**: Order confirmation in customer's language

---

## Testing the System

1. **Go to Menu Page**: http://localhost:2005/menu/
2. **Click "Add to Order"** on any menu item
3. **Select Order Type**:
   - For seated: Fill table number + guest name
   - For online: Fill email + phone + guest name
4. **Click "Create Order"**
5. **Check Admin Panel**: http://localhost:2005/admin/restaurant/order/
   - New order should appear in list

---

## Data Integrity

✅ Required fields validation (guest name, email for online, etc.)  
✅ Type validation (email, phone, numbers)  
✅ CSRF protection on form submission  
✅ Audit trail (created_at, updated_at timestamps)  
✅ Soft deletes possible (status = 'cancelled' instead of delete)  

---

## Integration Notes

The Order system is:
- ✅ Independent (doesn't require other features)
- ✅ Modular (can be extended with payments, delivery, etc.)
- ✅ Scalable (indexed by date, status, type for fast queries)
- ✅ Extensible (OrderItem allows multiple items per order)

---

Generated: December 28, 2025
Restaurant: Sip and Sunshine (Belgian Breakfast & BBQ)
