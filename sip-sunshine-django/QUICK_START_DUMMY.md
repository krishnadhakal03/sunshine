# ⚡ QUICK START - Populate Dummy Data (2 Minutes)

## Do This Right Now

### Step 1: Open Terminal
```bash
cd f:\sunshine\sip-sunshine-django
```

### Step 2: Run Setup
```bash
python setup_db.py
```

### Step 3: Done! ✅

You'll see output like:
```
============================================================
Setting up Sip and SunShine Restaurant Database
============================================================
...
✓ Database setup completed successfully!
============================================================
```

---

## Verify It Worked (30 seconds)

### Check 1: Admin Panel
1. Go to: `http://localhost:2005/admin/`
2. Login: `admin` / `admin123456`
3. Click **Site Settings** (under Restaurant)
4. See populated data ✅

### Check 2: Contact Page
1. Go to: `http://localhost:2005/contact/`
2. See address, phone, email cards ✅
3. See Google Map ✅

### Check 3: Reservation Page
1. Go to: `http://localhost:2005/reservation/`
2. See form and hours ✅

---

## Dummy Data You'll See

```
Email:   info@sipandsunshine.com
Phone:   +31 (0)20 123 4567
Address: 45 Prinsengracht, 1015 DK Amsterdam, Netherlands
Map:     Google Map of Amsterdam ✅
```

---

## When You Have Real Data

1. Go to: `http://localhost:2005/admin/`
2. Click **Site Settings**
3. Replace each field:
   - Email → customer's email
   - Phone → customer's phone
   - Address → customer's address
   - Map → get from Google Maps (see DUMMY_DATA_SETUP.md)
4. Click **Save** ✅

---

## Done! 🎉

Your Contact and Reservation pages now display with:
- ✅ Contact info
- ✅ Google Map
- ✅ Professional design
- ✅ Mobile responsive

**Replace dummy data with real info when ready!**

---

See `DUMMY_DATA_SETUP.md` for detailed instructions.
