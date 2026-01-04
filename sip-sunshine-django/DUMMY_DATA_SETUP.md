# Populate Dummy Data - Quick Start Guide

## Overview
This guide shows you how to populate your Django admin with realistic dummy data for testing the Contact and Reservation pages.

---

## Prerequisites

Make sure you have:
1. ✅ Django server running on port 2005
2. ✅ Database migrated (`python manage.py migrate`)
3. ✅ Admin user created (`python manage.py createsuperuser`)

---

## Option 1: Run Setup Script (Recommended)

### Step 1: Open Terminal
Navigate to your project folder:
```bash
cd f:\sunshine\sip-sunshine-django
```

### Step 2: Run the Setup Script
```bash
python setup_db.py
```

**Expected Output:**
```
============================================================
Setting up Sip and SunShine Restaurant Database
============================================================

[LANGUAGES] Setting up languages...
  - English: Created
  - Dutch (Nederlands): Created
  - French (Francais): Created

[SETTINGS] Setting up site settings...
  - Site settings: Created (or Updated with new dummy data)

[PAGES] Creating pages...
  - home: Already exists
  - about: Already exists
  - menu: Already exists
  - blog: Already exists
  - contact: Already exists
  - reservation: Already exists

✓ Creating menu items...
  - Caesar Salad: Created
  - Grilled Salmon: Created
  - Ribeye Steak: Created
  - Chocolate Lava Cake: Created
  - Fresh Orange Juice: Created
  - House Red Wine: Created

============================================================
✓ Database setup completed successfully!
============================================================
```

### Step 3: Verify It Worked
1. Open: `http://localhost:2005/admin/`
2. Login: `admin` / `admin123456`
3. Click **Site Settings** under **Restaurant**
4. You should see:
   - Email: `info@sipandsunshine.com`
   - Phone: `+31 (0)20 123 4567`
   - Address: `45 Prinsengracht, 1015 DK Amsterdam, Netherlands`
   - Google Map embed code populated

---

## Option 2: Run Alternative Script

If Option 1 doesn't work:

```bash
python populate_dummy_data.py
```

This does the same thing with more detailed output.

---

## Dummy Data That Gets Added

### Site Settings
| Field | Dummy Value |
|-------|------------|
| Site Name | Sip and SunShine |
| Email | info@sipandsunshine.com |
| Phone | +31 (0)20 123 4567 |
| Address | 45 Prinsengracht, 1015 DK Amsterdam, Netherlands |
| Facebook | https://facebook.com/sipandsunshine |
| Instagram | https://instagram.com/sipandsunshine |
| Twitter | https://twitter.com/sipandsunshine |
| Google Map | Full iframe embed code for Amsterdam location |
| Description | "Welcome to Sip and SunShine - Your premier Belgian restaurant specializing in breakfast, BBQ, and craft drinks..." |

### Menu Items (6 items)
1. **Caesar Salad** - €8.50 (Appetizers)
2. **Grilled Salmon** - €18.50 (Main Courses)
3. **Ribeye Steak** - €22.00 (Main Courses)
4. **Chocolate Lava Cake** - €7.50 (Desserts)
5. **Fresh Orange Juice** - €3.50 (Beverages)
6. **House Red Wine** - €5.00 (Drinks)

### Languages
- English (en) - Default
- Dutch (nl)
- French (fr)

---

## What Happens Next

After running the script:

### Contact Page
Visit: `http://localhost:2005/contact/`

You'll see:
- ✅ Contact form
- ✅ Address card showing: "45 Prinsengracht, 1015 DK Amsterdam, Netherlands"
- ✅ Phone card showing: "+31 (0)20 123 4567"
- ✅ Email card showing: "info@sipandsunshine.com"
- ✅ Google Map of Amsterdam embedded
- ✅ Professional styling with red accents

### Reservation Page
Visit: `http://localhost:2005/reservation/`

You'll see:
- ✅ Reservation form
- ✅ Opening hours
- ✅ Professional styling

---

## Replace Dummy Data with Real Data

When you're ready to use real information:

### Method 1: Admin Panel (Recommended)
1. Go to: `http://localhost:2005/admin/`
2. Click **Site Settings**
3. Edit each field with real data:
   - Email → Your real email
   - Phone → Customer's phone
   - Address → Customer's address
   - Google Map → Get real embed code (see instructions below)
4. Click **Save**

### Method 2: Direct Database Edit (Advanced)
Edit the values directly in the database via admin panel.

### Getting Real Google Map Embed Code

1. Go to: https://maps.google.com
2. Search for the restaurant address
3. Click the **Share** button (top left)
4. Click **Embed a map** tab
5. Copy the entire `<iframe>` code
6. In admin: Site Settings → Google Map Embed field
7. Paste the code
8. Save

**Example:**
```html
<iframe src="https://www.google.com/maps/embed?pb=..." 
        width="600" height="450" style="border:0;" 
        allowfullscreen="" loading="lazy" 
        referrerpolicy="no-referrer-when-downgrade"></iframe>
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution**: Make sure Django is installed
```bash
pip install django
```

### Issue: "LookupError: No installed app with label 'restaurant'"
**Solution**: Migrations haven't been run yet
```bash
python manage.py migrate
```

### Issue: "SiteSetting matching query does not exist"
**Solution**: The script will create it. If this error persists, check database is migrated.

### Issue: Script runs but data doesn't appear in admin
**Solution**: 
1. Refresh the page (Ctrl+F5)
2. Clear browser cache
3. Check Django terminal for errors
4. Restart Django server

### Issue: Google Map showing as text instead of embed
**Solution**: 
1. Check that the iframe code was pasted correctly
2. Ensure it's complete with `<iframe>` tags
3. The `|safe` filter in template allows HTML rendering

---

## Verifying Data Was Added

### Via Admin Panel
1. Open: `http://localhost:2005/admin/`
2. Under **Restaurant**, click **Site Settings**
3. Verify all fields are populated

### Via Contact Page
1. Open: `http://localhost:2005/contact/`
2. Look for contact info cards
3. Verify address, phone, email display
4. Verify map shows

### Via Database Shell
```bash
python manage.py shell
```

Then:
```python
from restaurant.models import SiteSetting
settings = SiteSetting.objects.first()
print(settings.email)        # Should print: info@sipandsunshine.com
print(settings.phone)        # Should print: +31 (0)20 123 4567
print(settings.address)      # Should print the Amsterdam address
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Run setup | `python setup_db.py` |
| Alternative setup | `python populate_dummy_data.py` |
| Start Django | `python manage.py runserver` |
| Access admin | http://localhost:2005/admin/ |
| View contact page | http://localhost:2005/contact/ |
| View reservation page | http://localhost:2005/reservation/ |
| Clear database | `python manage.py flush` |
| Database shell | `python manage.py shell` |

---

## Timeline: Dummy → Real Data

1. **Now**: Run setup script → Dummy data added
2. **Today**: Test pages with dummy data
3. **This Week**: Collect real data from customer
4. **Next Week**: Replace dummy data via admin
5. **Launch**: Go live with real data

---

## What's in the Dummy Data

### Contact Information
- Professional restaurant description
- Realistic Amsterdam address
- Valid Dutch phone format
- Contact email
- Social media links
- Working Google Map embed

### Menu Items
- 6 sample dishes/drinks
- Realistic pricing
- Professional descriptions
- Multi-language support

### Pages
- All required pages created
- Multi-language translations
- Proper metadata for SEO
- Correct templates assigned

---

## Next Steps After Setup

1. ✅ Run setup script
2. ✅ Visit admin and verify data
3. ✅ Visit contact page and check display
4. ✅ Visit reservation page and check display
5. ✅ Test form submissions
6. ✅ Take screenshots to show customer
7. ✅ Collect real data from customer
8. ✅ Update in admin with real values
9. ✅ Go live!

---

## Support

If you encounter issues:
1. Check Django terminal for error messages
2. Verify database is migrated
3. Clear browser cache and refresh
4. Restart Django server
5. Check that static files are served

---

**Status**: Ready to populate! Run `python setup_db.py` now to see your pages in action! 🚀

