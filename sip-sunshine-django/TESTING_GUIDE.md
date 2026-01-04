# Visual & Setup Guide - Contact & Reservation Pages

## Testing the Pages

### Prerequisites
1. Django server running: `python manage.py runserver`
2. Access: `http://localhost:2005/`

---

## Contact Page - What You Should See

### URL: `http://localhost:2005/contact/`

```
┌─────────────────────────────────────────┐
│  [NAV BAR with Logo and Menu]           │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│                                         │
│    CONTACT US                           │
│    Home / Contact                       │
│                                         │
│    (Red gradient background)            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│                                         │
│  [FORM SECTION]          [MAP SECTION]  │
│                                         │
│  Get In Touch             (Google Map   │
│  ─────────────            or default)   │
│                                         │
│  Your Name:  [_________]               │
│  Your Email: [_________]               │
│  Phone:      [_________]               │
│  Subject:    [_________]               │
│  Message:    [_________]               │
│               [_________]              │
│                                        │
│  [Send Message Button]                 │
│                                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Contact Information                     │
│ We're here to help...                   │
│ ───────────────────────────────────────│
│                                        │
│ [ADDRESS]  [PHONE]  [EMAIL]           │
│ Card       Card      Card              │
│                                        │
│ 123 Res... +31(0)6.. info@...         │
│                                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ [Full-width Google Map Embed]          │
│ or                                      │
│ Map placeholder message                │
└─────────────────────────────────────────┘
```

**What Should Display:**
- ✅ Gradient red hero banner with "CONTACT US"
- ✅ Form on left, map on right (desktop)
- ✅ Form on top, map below (mobile)
- ✅ Three information cards below form
- ✅ Contact details in cards
- ✅ Google Map at bottom (if configured)

**If Pages Appear Empty:**
1. Check browser console for errors (F12)
2. Verify `site_settings` is configured in admin
3. See "Troubleshooting" section below

---

## Reservation Page - What You Should See

### URL: `http://localhost:2005/reservation/`

```
┌─────────────────────────────────────────┐
│  [NAV BAR with Logo and Menu]           │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│                                         │
│    BOOK A TABLE                         │
│    Home / Reservation                   │
│                                         │
│    (Red gradient background)            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│                                         │
│    Reserve Your Table                   │
│                                         │
│    Fill in the form below...            │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Your Name *:     [________]      │  │
│  │  Email *:         [________]      │  │
│  │  Phone *:         [________]      │  │
│  │                                   │  │
│  │  Date *:  [____]  Time *: [____]  │  │
│  │                                   │  │
│  │  Number of Guests *: [__]         │  │
│  │                                   │  │
│  │  Special Requests:                │  │
│  │  [________________]               │  │
│  │  [________________]               │  │
│  │                                   │  │
│  │  [RESERVE NOW Button]             │  │
│  └──────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│                                         │
│    Opening Hours                        │
│    ───────────────                      │
│                                         │
│    ┌────────────────────────────────┐  │
│    │ Monday to Thursday             │  │
│    │ 11:00 AM - 10:00 PM            │  │
│    │ ─────────────────────────────  │  │
│    │ Friday to Sunday               │  │
│    │ 11:00 AM - 11:00 PM            │  │
│    │ ─────────────────────────────  │  │
│    │ Closed on major holidays       │  │
│    └────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

**What Should Display:**
- ✅ Gradient red hero banner with "BOOK A TABLE"
- ✅ Centered reservation form
- ✅ Required field markers (*)
- ✅ Date and time inputs
- ✅ Number of guests input
- ✅ Special requests textarea
- ✅ Opening hours in red gradient box
- ✅ Professional spacing and styling

---

## Troubleshooting

### Issue 1: Pages Appear Empty or Unstyled

**Cause**: CSS not loading or view not returning content

**Solution**:
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Clear browser cache (Ctrl+Shift+Delete)
4. Refresh page (Ctrl+F5)
5. Check that static files are served:
   ```
   python manage.py collectstatic
   ```

### Issue 2: Contact Cards Show Default Text

**Cause**: `site_settings` not configured in admin

**Solution**:
1. Go to: `http://localhost:2005/admin/`
2. Login with admin / admin123456
3. Click "Site Settings" under Restaurant
4. Fill in: Address, Phone, Email
5. Click Save
6. Refresh contact page (F5)

### Issue 3: Map Section Shows Placeholder

**Cause**: Google Map embed code not configured

**Solution**:
1. Go to [Google Maps](https://maps.google.com)
2. Search for your restaurant location
3. Click "Share" → "Embed a map"
4. Copy the iframe code
5. In admin: Site Settings → Google Map Embed field
6. Paste the iframe code
7. Click Save
8. Refresh contact page (F5)

### Issue 4: Form Not Submitting

**Cause**: Django form handling or redirect issue

**Check**:
1. Open DevTools (F12) → Network tab
2. Fill form and submit
3. Check if POST request is made
4. Look for success message on page
5. Check terminal for Django errors

**Fix**:
1. Ensure form has `method="POST"` ✅
2. Ensure form has `{% csrf_token %}` ✅
3. Check view handles POST correctly ✅
4. Verify email/phone settings if error

### Issue 5: Mobile View Broken

**Cause**: CSS media queries not applied

**Solution**:
1. Open DevTools (F12)
2. Click mobile phone icon (responsive mode)
3. Test at different widths
4. Check that layout stacks on small screens
5. Verify form inputs are readable

### Issue 6: Icons Not Showing

**Cause**: Icomoon font not loaded

**Check**:
1. Open DevTools Console
2. Look for 404 errors on fonts
3. Check static files folder exists
4. Run: `python manage.py collectstatic`
5. Restart Django server

---

## Admin Configuration Steps

### Step-by-Step Setup

1. **Start Django**:
   ```bash
   python manage.py runserver
   ```

2. **Open Admin Panel**:
   - URL: `http://localhost:2005/admin/`
   - Username: `admin`
   - Password: `admin123456`

3. **Navigate to Site Settings**:
   - In left menu: "Restaurant" → "Site Settings"
   - Click the existing setting (there's only one)

4. **Fill in Contact Information**:
   - **Email**: `info@sipandsunshine.com`
   - **Phone**: `+31 (0)6 12345678`
   - **Address**: `123 Restaurant Street, Amsterdam, Netherlands`

5. **Add Google Map** (optional):
   - Go to https://maps.google.com
   - Search your restaurant address
   - Click Share → Embed a map
   - Copy the `<iframe>` code
   - Paste in "Google Map Embed" field

6. **Save Changes**:
   - Scroll to bottom
   - Click blue "SAVE" button

7. **Test**:
   - Open: `http://localhost:2005/contact/`
   - Verify cards show your info
   - Verify map appears (if configured)

---

## Quick Checklist

Before considering pages complete:

- [ ] Contact page displays
- [ ] Form labels visible
- [ ] Form inputs have focus effect (red border)
- [ ] Contact info cards show address, phone, email
- [ ] Map appears or placeholder shows
- [ ] Reservation page displays
- [ ] Reservation form shows all fields
- [ ] Opening hours display in red box
- [ ] Both pages look good on mobile
- [ ] Submit buttons work without page reload
- [ ] Success messages appear after form submit

---

## Performance Tips

✅ **Static Files**: Cached by browser  
✅ **CSS**: Inline in templates for faster load  
✅ **JavaScript**: Minimal, using jQuery from Bootstrap  
✅ **Images**: Optimized (SVG for logo/favicon)  
✅ **Forms**: Client-side validation before submit  

---

## Browser Testing

Test on these browsers to ensure compatibility:

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iPhone)
- [ ] Chrome Mobile (Android)

---

## Support

If pages still appear empty after following this guide:

1. **Check terminal output** for Django errors
2. **View page source** (Ctrl+U) to see HTML structure
3. **Check static files** are in `static/` folder
4. **Verify migrations** with: `python manage.py migrate`
5. **Run setup** with: `python setup_db.py`

---

## Summary

Both pages should now display:
- ✅ Modern, professional design
- ✅ Red accent color (#f34949)
- ✅ Responsive layout (desktop & mobile)
- ✅ Smooth animations
- ✅ Professional typography
- ✅ Contact information (once configured)
- ✅ Working forms with validation

For detailed admin setup, see: **ADMIN_SETUP_GUIDE.md**

