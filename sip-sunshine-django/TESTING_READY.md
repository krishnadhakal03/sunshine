# System Ready for Testing - Complete Guide

## Status: READY FOR TESTING ✅

### What's Been Done
- ✅ Database migrations completed
- ✅ Test data created in database
- ✅ Admin configuration fixed
- ✅ All system checks passed

### Test Orders Already Created
The system has been pre-populated with test data:

**Order #1 - SEATED ORDER**
- Guest: John Smith
- Email: john@example.com
- Phone: 555-1234
- Table: 5
- Item: Grilled Steak (qty 2)
- Status: Pending

**Order #2 - ONLINE ORDER**
- Guest: Jane Doe
- Email: jane@example.com
- Phone: 555-5678
- Delivery: 123 Main Street, New York, 10001, USA
- Items: Pasta Carbonara (qty 1), Caesar Salad (qty 1)
- Status: Pending

---

## How to Run Locally

### Step 1: Start Django Server
```bash
cd f:\sunshine\sip-sunshine-django
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 2: Test the System

#### Test URLs
Open in browser:
- **Menu**: http://localhost:8000/menu/
- **Login**: http://localhost:8000/auth/login/
- **Register**: http://localhost:8000/auth/register/
- **Profile**: http://localhost:8000/auth/profile/ (after login)
- **Tracking**: http://localhost:8000/orders/tracking/
- **Admin**: http://localhost:8000/admin/

#### Admin Credentials
- Username: `krishna` (or `testcustomer`)
- Password: (your admin password or `TestPass123` for testcustomer)

---

## Manual Testing Workflow

### Test 1: View Seated Order (Already Created)
```
1. Go to http://localhost:8000/orders/tracking/
2. Enter Order ID: 1
3. Verify display shows:
   - Order #1
   - Guest: John Smith
   - Table: 5
   - Item: Grilled Steak x2
   - Status: Pending
```

### Test 2: View Online Order (Already Created)
```
1. Go to http://localhost:8000/orders/tracking/
2. Enter Order ID: 2
3. Verify display shows:
   - Order #2
   - Guest: Jane Doe
   - Delivery Address: 123 Main Street, New York, 10001, USA
   - Items: Pasta Carbonara x1, Caesar Salad x1
   - Status: Pending
```

### Test 3: Create New Seated Order from Menu
```
1. Go to http://localhost:8000/menu/
2. Click "Add to Order" on any menu item
3. Modal should appear with:
   - Item image
   - Item name
   - Item price
4. Select "Seated" order type
5. Fill form:
   - Guest Name: "Test Guest"
   - Table Number: 8 (optional)
   - Quantity: 2
6. Click "Confirm Order"
7. See confirmation page with new Order ID
8. Go to /orders/tracking/ and search for this Order ID
9. Verify all details display correctly
```

### Test 4: Create New Online Order from Menu
```
1. Go to http://localhost:8000/menu/
2. Click "Add to Order" on different item
3. Modal appears
4. Select "Online" order type
5. IMPORTANT: All address fields must show
6. Fill form:
   - Guest Name: "Online Test"
   - Email: "online@test.com"
   - Phone: "555-9999"
   - Address: "456 Oak Ave"
   - City: "Los Angeles"
   - Postal Code: "90001"
   - Country: "USA"
   - Quantity: 1
7. Click "Confirm Order"
8. See confirmation with delivery address
9. Go to /orders/tracking/ with new Order ID
10. Verify address displays correctly
```

### Test 5: Admin Interface
```
1. Go to http://localhost:8000/admin/
2. Login with admin credentials
3. Navigate to Restaurant > Orders
4. Verify both pre-created orders display:
   - Order #1 (Seated)
   - Order #2 (Online)
5. Click on Order #1:
   - Should show table_number: 5
   - Address fields should be empty
6. Click on Order #2:
   - Should show delivery_address, city, postal_code, country
   - Table number field should be empty
7. Try editing order status and save
8. Go back to list
9. Try using filters (Status, Order Type)
10. Try search (by name, email)
```

### Test 6: Authentication (Optional)
```
1. Go to http://localhost:8000/auth/register/
2. Create new account:
   - Full Name: "Test User"
   - Email: "testuser@example.com"
   - Phone: "555-0000"
   - Password: "TestPass123!"
3. Should redirect to login
4. Go to /auth/login/ and login
5. Should redirect to /auth/profile/
6. Should show profile with order history
```

---

## What to Verify

### Menu Modal
- [ ] "Add to Order" button works
- [ ] Modal appears with item details
- [ ] Item image displays (if available)
- [ ] Item name and price show correctly
- [ ] Quantity +/- buttons work
- [ ] Seated/Online toggle switches fields

### Seated Order
- [ ] Guest name field required
- [ ] Table number field appears (optional)
- [ ] Address fields hidden
- [ ] Form submits without page reload
- [ ] Confirmation shows table number
- [ ] Confirmation hides address
- [ ] Tracking page shows table info

### Online Order
- [ ] Guest name field required
- [ ] All address fields required
- [ ] Table field hidden
- [ ] Email validation works
- [ ] Form won't submit with missing fields
- [ ] Confirmation shows full address
- [ ] Tracking page shows delivery address

### Admin Interface
- [ ] Orders display in list
- [ ] Seated orders show table number
- [ ] Online orders show all address fields
- [ ] Can edit order status
- [ ] Can search by name/email/phone
- [ ] Can filter by status/type/date
- [ ] OrderItems display inline

### Database
- [ ] Address fields saved (online orders only)
- [ ] All orders queryable
- [ ] Order items linked correctly
- [ ] Status updates persist

---

## Troubleshooting

### Issue: Modal doesn't appear
**Solution**: 
- Check browser F12 console for errors
- Verify JavaScript loaded (Network tab)
- Clear cache: Ctrl+Shift+Delete
- Reload page

### Issue: Order not saving
**Solution**:
- Check form validation errors
- Verify all required fields filled
- Check browser console
- Try a different item

### Issue: Address fields not showing for online orders
**Solution**:
- Select "Online" radio button
- Wait for form to update
- Clear cache and reload
- Try different browser

### Issue: Admin shows no orders
**Solution**:
- Verify you're at /admin/restaurant/order/
- Verify OrderAdmin registered in admin.py
- Check database (orders do exist)

### Issue: Orders not tracking
**Solution**:
- Use correct Order ID (1 or 2)
- Check URL: /orders/tracking/
- Try creating new order first

---

## Quick Reference

### Database Status
- Migrations: ✅ COMPLETED
- Test Orders: ✅ CREATED (Order #1 Seated, Order #2 Online)
- Admin: ✅ READY

### Components Status
- Menu Modal: ✅ INTEGRATED
- JavaScript: ✅ INCLUDED
- Templates: ✅ CREATED
- Views: ✅ CONFIGURED
- URLs: ✅ ROUTED
- Admin: ✅ REGISTERED

### Key Files
- `templates/pages/menu.html` - Menu page (UPDATED)
- `templates/orders/order_modal.html` - Order form
- `static/js/order-system.js` - Client-side logic
- `restaurant/views.py` - Backend views
- `restaurant/admin.py` - Admin interface
- `restaurant/models.py` - Data models

---

## Expected Results

After testing, you should see:

1. **Menu Page**: Works normally with "Add to Order" buttons
2. **Modal**: Opens with item details
3. **Form Submission**: Works without page reload (AJAX)
4. **Confirmation**: Shows order details with correct info
5. **Tracking**: Displays order status for both seated and online
6. **Admin**: Shows all orders with proper field display
7. **Search/Filter**: Works in admin interface
8. **Mobile**: All pages responsive

---

## Next Steps After Testing

1. If all tests pass:
   - System is production-ready
   - Deploy to production
   - Train staff on admin interface

2. If issues found:
   - Document the issue
   - Check browser console
   - Review Django logs
   - Contact for support

---

**Status**: Ready for comprehensive testing!

Start by running `python manage.py runserver` and visiting the URLs listed above.
