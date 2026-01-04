# Sip and SunShine Restaurant - Quick Start Guide

## 🚀 Getting Started (Fast Track)

### For Windows Users:
```bash
1. Open Command Prompt/PowerShell
2. Navigate to: f:\sunshine\sip-sunshine-django
3. Run: quickstart.bat
4. Follow the prompts
```

### For macOS/Linux Users:
```bash
1. Open Terminal
2. Navigate to: /path/to/sip-sunshine-django
3. Run: bash quickstart.sh
4. Follow the prompts
```

## 📋 Manual Setup (Step by Step)

### Step 1: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Apply Database Migrations
```bash
python manage.py migrate
```

**Output should show:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ... (more migrations)
  Applying restaurant.0001_initial... OK
```

### Step 4: Initialize Sample Data
```bash
python setup_db.py
```

**Output should show:**
```
============================================================
Setting up Sip and SunShine Restaurant Database
============================================================

✓ Setting up languages...
  - English: Created
  - Dutch (Nederlands): Created
  - French (Français): Created

✓ Setting up site settings...
  - Site settings: Created

✓ Creating pages...
  - home: Created
  - about: Created
  - menu: Created
  - blog: Created
  - contact: Created
  - reservation: Created

✓ Creating menu items...
  - Caesar Salad: Created
  - Grilled Salmon: Created
  ... (more items)

============================================================
✓ Database setup completed successfully!
============================================================
```

### Step 5: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@sipandsunshine.com
Password: (your secure password)
Password (again): (confirm)
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 7: Access Your Website

**Frontend:**
- Home: http://localhost:8000/
- Menu: http://localhost:8000/menu/
- About: http://localhost:8000/about/
- Blog: http://localhost:8000/blog/
- Contact: http://localhost:8000/contact/
- Reservation: http://localhost:8000/reservation/

**Admin Panel:**
- URL: http://localhost:8000/admin/
- Username: `admin` (what you created in Step 5)
- Password: Your password from Step 5

## 🌐 Multi-Language Testing

### Language URLs:
- English: `http://localhost:8000/` or `http://localhost:8000/en/`
- Dutch: `http://localhost:8000/nl/`
- French: `http://localhost:8000/fr/`

### Language Switcher:
- Use the language dropdown in the top navigation bar
- Click English, Dutch, or French to switch

## 📁 Important File Locations

| File | Purpose |
|------|---------|
| `manage.py` | Django management commands |
| `requirements.txt` | Python dependencies |
| `setup_db.py` | Initialize database with sample data |
| `restaurant/models.py` | Database models (Page, MenuItem, BlogPost, etc.) |
| `restaurant/views.py` | View logic |
| `restaurant/admin.py` | Admin interface config |
| `templates/base.html` | Base template (header, footer, navigation) |
| `templates/pages/` | Page-specific templates |
| `static/css/` | CSS stylesheets |
| `static/js/` | JavaScript files |
| `static/images/` | Images |
| `media/` | User-uploaded files (images, etc.) |

## ⚙️ Configuration Files

### Django Settings
- **Base Settings**: `sip_sunshine/settings/base.py`
- **Development Settings**: `sip_sunshine/settings/development.py`

Key settings:
```python
DEBUG = True                          # Development mode
ALLOWED_HOSTS = ['*']                # Accept all hosts in dev
LANGUAGE_CODE = 'en'                 # Default language
DATABASES = {...}                    # SQLite database
```

## 🎨 Customizing Your Site

### Change Site Name & Logo

1. Go to: http://localhost:8000/admin/
2. Click: **Restaurant > Site settings**
3. Edit:
   - Site Name: "Sip and SunShine"
   - Logo: Upload your restaurant logo
   - Email: Your contact email
   - Phone: Your phone number
   - Address: Your restaurant address

### Add Menu Items

1. Admin Panel > **Restaurant > Menu items**
2. Click **Add Menu Item**
3. Fill in:
   - Category (Appetizers, Main Courses, Desserts, Beverages, Drinks)
   - Name (English)
   - Description (English)
   - Price
   - Image (optional)
4. Click "Save and Continue Editing"
5. Switch to Dutch tab and fill in Dutch translations
6. Switch to French tab and fill in French translations
7. Click "Save"

### Create New Blog Post

1. Admin Panel > **Restaurant > Blog posts**
2. Click **Add Blog Post**
3. Fill in:
   - Title (English)
   - Author name
   - Featured Image
   - Excerpt (summary)
   - Content (full article)
   - Meta Description & Keywords
4. Switch to Dutch and French tabs to add translations
5. Set as Published and Published Date
6. Click "Save"

### Edit Pages

1. Admin Panel > **Restaurant > Pages**
2. Choose page (Home, About, Menu, Contact, etc.)
3. Edit content in each language
4. Update SEO settings (Meta Title, Description, Keywords)
5. Click "Save"

## 🔍 Testing Features

### Test Contact Form
1. Visit: http://localhost:8000/contact/
2. Fill in form with test data
3. Submit
4. Check admin: **Restaurant > Contact messages**

### Test Reservation System
1. Visit: http://localhost:8000/reservation/
2. Fill in reservation form
3. Submit
4. Check admin: **Restaurant > Reservations**

### Test Multi-Language
1. Visit homepage
2. Click language dropdown (top right)
3. Select language
4. Content should change language

## 📊 Database Check

To see what's in your database:

1. Admin Panel: http://localhost:8000/admin/
2. Click each section to view/edit:
   - **Languages**: Should show English, Dutch, French
   - **Site Settings**: Your restaurant information
   - **Pages**: All 6 pages (Home, About, Menu, Blog, Contact, Reservation)
   - **Menu Items**: Your menu items with prices
   - **Content Blocks**: Reusable content sections
   - **Blog Posts**: Articles you've created
   - **Reservations**: Booking requests from visitors
   - **Contact Messages**: Messages from contact form

## 🐛 Common Issues & Solutions

### Issue: "Module not found" error
**Solution:**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: "No such table" error
**Solution:**
```bash
# Re-run migrations
python manage.py migrate
```

### Issue: Images not showing
**Solution:**
1. Copy Kusina template files:
   ```bash
   # Windows
   xcopy f:\sunshine\kusina-master\css\* static\css\ /Y
   xcopy f:\sunshine\kusina-master\js\* static\js\ /Y
   xcopy f:\sunshine\kusina-master\images\* static\images\ /Y
   ```

### Issue: Admin login not working
**Solution:**
```bash
# Create new superuser
python manage.py createsuperuser
```

### Issue: Language not changing
**Solution:**
1. Clear browser cache
2. Check admin > Languages (should have 3 active languages)
3. Try incognito/private browser window

## 📝 Notes

- **Database File**: `db.sqlite3` (created after migration)
- **Static Files**: `static/` folder
- **User Uploads**: `media/` folder
- **Python Version**: Requires Python 3.8+
- **Email**: Currently prints to console (configure SMTP for production)

## 🎯 Next Testing Steps

After running the application:

1. ✅ Test homepage loads
2. ✅ Test all pages accessible
3. ✅ Test language switching
4. ✅ Test menu display
5. ✅ Test blog posts
6. ✅ Test contact form
7. ✅ Test reservation form
8. ✅ Test admin panel
9. ✅ Test adding/editing content
10. ✅ Test image uploads

## 📞 Support

When you encounter issues or need to test something specific, refer to:
- `README.md` - Full documentation
- `restaurant/models.py` - Data structure
- `restaurant/admin.py` - Admin configuration
- Django Docs: https://docs.djangoproject.com/

---

**Everything is ready! Run the application and test all functionality.** 🚀
