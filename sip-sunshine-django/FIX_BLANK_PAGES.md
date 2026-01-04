# 🔧 Fix Blank Pages - Troubleshooting Guide

## If Pages Are Still Blank or Empty

### Issue 1: Reservation Page Shows Nothing

**Cause**: Page record doesn't exist in database

**Fix** (Try each step):

#### Step 1: Create Missing Page Records
```bash
python fix_blank_pages.py
```

#### Step 2: Run Full Setup
If Step 1 doesn't work:
```bash
python setup_db.py
```

#### Step 3: Check Admin
1. Go to: `http://localhost:2005/admin/`
2. Click: **Pages** (under Restaurant)
3. Look for: "reservation" and "contact"
4. If missing: Create them manually
   - Slug: `reservation`
   - Template: `reservation`
   - Active: ✅ Yes
5. Click: **Save**

---

### Issue 2: Contact Page Right Section Empty

**Cause**: Google Map embed code not configured

**Status**: ✅ This is now FIXED

The right section now shows:
- ✅ Google Map if configured
- ✅ Placeholder message if not configured

**To Add Real Map**:
1. Go to: `http://localhost:2005/admin/`
2. Click: **Site Settings**
3. Find field: **Google Map Embed**
4. Get embed code from:
   - Go to: https://maps.google.com
   - Search restaurant address
   - Click **Share** → **Embed a map**
   - Copy `<iframe>` code
5. Paste in **Google Map Embed** field
6. Click **Save** ✅

---

### Issue 3: Forms Not Displaying

**Cause**: Page template not loading correctly

**Check**:
1. Open DevTools (F12)
2. Go to **Console** tab
3. Look for red error messages
4. Take screenshot and check
5. If errors exist, report them

**Fix**:
```bash
# Clear cache and restart
python manage.py collectstatic
python manage.py runserver
```

Then refresh page (Ctrl+F5)

---

### Issue 4: Both Pages Completely Blank

**Most Likely Cause**: Database not migrated OR setup not run

**Fix**:

Step 1: Migrate database
```bash
python manage.py migrate
```

Step 2: Populate dummy data
```bash
python setup_db.py
```

Step 3: Create missing pages
```bash
python fix_blank_pages.py
```

Step 4: Restart Django
```bash
# Stop: Ctrl+C
python manage.py runserver
```

Step 5: Visit pages
- Contact: `http://localhost:2005/contact/`
- Reservation: `http://localhost:2005/reservation/`

---

## What Should Display Now

### ✅ Contact Page Layout

```
┌──────────────────────────────────────────────┐
│ Hero Banner: "CONTACT US"                    │
└──────────────────────────────────────────────┘
┌──────────────────────┬──────────────────────┐
│ Form                 │ Map or Placeholder   │
│ - Name              │ - Shows Google Map   │
│ - Email             │   (if configured)    │
│ - Phone             │ - Or placeholder msg │
│ - Subject           │                      │
│ - Message           │                      │
│ [Send Button]       │                      │
└──────────────────────┴──────────────────────┘
┌──────────────────────────────────────────────┐
│ Address Card | Phone Card | Email Card       │
└──────────────────────────────────────────────┘
```

### ✅ Reservation Page Layout

```
┌──────────────────────────────────────────────┐
│ Hero Banner: "BOOK A TABLE"                  │
└──────────────────────────────────────────────┘
┌──────────────────────────────────────────────┐
│ Reserve Your Table                           │
│ [Centered Form]                              │
│ - Name *                                     │
│ - Email * | Phone *                          │
│ - Date * | Time *                            │
│ - Number of Guests *                         │
│ - Special Requests                           │
│ [Reserve Now Button]                         │
└──────────────────────────────────────────────┘
┌──────────────────────────────────────────────┐
│ Opening Hours (Red Box)                      │
│ Monday-Thursday: 11 AM - 10 PM              │
│ Friday-Sunday: 11 AM - 11 PM                │
└──────────────────────────────────────────────┘
```

---

## Quick Checklist

After running fixes, verify:

- [ ] Run: `python setup_db.py`
- [ ] Run: `python fix_blank_pages.py`
- [ ] Restart Django server
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Visit: `http://localhost:2005/contact/`
- [ ] Visit: `http://localhost:2005/reservation/`
- [ ] Check both pages display content
- [ ] Check forms appear
- [ ] Check opening hours display
- [ ] Check contact info cards display

---

## Admin Verification

1. Go to: `http://localhost:2005/admin/`
2. Login: `admin` / `admin123456`
3. Check these sections:

**Pages Section**:
- [ ] Click "Pages"
- [ ] See "contact" page
- [ ] See "reservation" page
- [ ] Both marked as Active (✅)

**Site Settings Section**:
- [ ] Click "Site Settings"
- [ ] See email populated
- [ ] See phone populated
- [ ] See address populated
- [ ] Optionally see Google Map embed code

If any are missing, create them manually or re-run setup scripts.

---

## If Still Not Working

Do this troubleshooting:

### Check 1: Database is Migrated
```bash
python manage.py migrate --check
```

Should output: `All migrations have been applied`

### Check 2: Django Has No Errors
Check terminal for errors when you visit the page

### Check 3: Static Files Collected
```bash
python manage.py collectstatic --noinput
```

### Check 4: Pages Table Has Records
```bash
python manage.py shell
# Then type:
from restaurant.models import Page
print(Page.objects.all())
# Should show: contact and reservation
```

### Check 5: Site Settings Exists
```bash
python manage.py shell
# Then type:
from restaurant.models import SiteSetting
print(SiteSetting.objects.first())
# Should show settings object
```

---

## Still Having Issues?

### If "Page matching query does not exist"
→ Run: `python fix_blank_pages.py`

### If Map section empty
→ This is NORMAL - add map in admin or run `python setup_db.py` for dummy map

### If forms don't submit
→ Check terminal for Django errors

### If nothing displays at all
→ Run: `python setup_db.py` then restart server

---

## Quick Commands Reference

```bash
# Populate everything (recommended)
python setup_db.py

# Fix blank pages
python fix_blank_pages.py

# Restart Django
Ctrl+C  # Stop current server
python manage.py runserver  # Start new server

# Collect static files
python manage.py collectstatic

# Migrate database
python manage.py migrate

# Check database
python manage.py shell
from restaurant.models import Page
print(Page.objects.all())
```

---

## Summary

### Pages are now fixed:
✅ Contact page shows form + info + map section
✅ Reservation page shows form + hours
✅ Right section of contact shows Google Map or placeholder

### If still blank:
1. Run: `python setup_db.py`
2. Run: `python fix_blank_pages.py`
3. Restart Django
4. Refresh browser

**Pages should display after these steps!**

