# QUICK START GUIDE

## Your Django Restaurant Website is Ready! 🚀

Your **Sip and SunShine** restaurant website is fully configured and ready to run locally.

---

## START THE SERVER

### Windows (Easiest):
```bash
# Double-click this file:
run_server.bat
```

### Command Line:
```bash
cd f:\sunshine\sip-sunshine-django
python manage.py runserver
```

---

## VISIT YOUR WEBSITE

Once the server starts, open your browser:

| Page | URL |
|------|-----|
| **Homepage (English)** | http://127.0.0.1:8000/ |
| **Dutch Version** | http://127.0.0.1:8000/nl/ |
| **French Version** | http://127.0.0.1:8000/fr/ |
| **Menu** | http://127.0.0.1:8000/menu/ |
| **Blog** | http://127.0.0.1:8000/blog/ |
| **Contact** | http://127.0.0.1:8000/contact/ |
| **Reservation** | http://127.0.0.1:8000/reservation/ |
| **Admin Panel** | http://127.0.0.1:8000/admin/ |

---

## LOGIN TO ADMIN

**URL**: http://127.0.0.1:8000/admin/

**Username**: `admin`  
**Password**: `admin123456`

From the admin panel you can:
- ✅ Edit pages and content
- ✅ Add/edit menu items (with translations)
- ✅ Create and publish blog posts
- ✅ Update site settings
- ✅ View contact form submissions
- ✅ View reservations

---

## WHAT'S INCLUDED

✅ **8 Database Models**
- Pages, Menu Items, Blog Posts, Content Blocks, Reservations, Contact Messages

✅ **Multi-Language Support**
- English, Dutch, French with automatic URL prefixing

✅ **Responsive Design**
- Bootstrap + Kusina Restaurant Template

✅ **All Template Assets**
- CSS (17 files), JavaScript (19 files), Images (75 files), Fonts (5 sets)

✅ **Admin Interface**
- Full CRUD operations for all content

✅ **Sample Data**
- 3 languages, 6 pages, menu items in all languages, site settings

---

## TROUBLESHOOTING

### Port Already in Use?
If port 8000 is busy, use a different port:
```bash
python manage.py runserver 8001
```
Then visit http://127.0.0.1:8001/

### Want to Reset Everything?
```bash
# Delete the database
del db.sqlite3

# Recreate it
python manage.py migrate
python setup_db.py
```

### Django System Check
To see if everything is configured correctly:
```bash
python manage.py check
```

---

## FOLDER STRUCTURE

```
f:\sunshine\sip-sunshine-django\
├── manage.py              # Django management
├── db.sqlite3            # Database (created)
├── run_server.bat        # Double-click to run
├── setup_db.py           # Initialize sample data
│
├── restaurant/           # Main Django app
│   ├── models.py        # 8 database models
│   ├── views.py         # 8 view classes
│   ├── admin.py         # Admin interface
│   └── migrations/      # Database schema
│
├── templates/           # HTML templates
│   ├── base.html       # Master template
│   └── pages/          # 8 page templates
│
└── static/             # All CSS, JS, images, fonts
    ├── css/           # 17 CSS files
    ├── js/            # 19 JavaScript files
    ├── images/        # 75 image files
    └── fonts/         # Font files
```

---

## MODIFY YOUR CONTENT

Everything is stored in the database:

1. **Edit Pages**: Admin → Pages
2. **Manage Menu**: Admin → Menu Items
3. **Add Blog Posts**: Admin → Blog Posts
4. **Update Settings**: Admin → Site Settings

All changes are immediately visible on the website!

---

## LANGUAGES

The website supports 3 languages:

- **English** (default, no prefix): /
- **Dutch**: /nl/
- **French**: /fr/

Use the language dropdown in the navbar to switch.

---

## TEST THE FORMS

1. **Contact Form** - http://127.0.0.1:8000/contact/
   - Submissions saved to database
   - View in Admin → Contact Messages

2. **Reservation Form** - http://127.0.0.1:8000/reservation/
   - Bookings saved to database
   - View in Admin → Reservations

---

## NEXT STEPS

### To Test:
- [ ] Run the server
- [ ] Visit http://127.0.0.1:8000/
- [ ] Try different language versions (/nl/, /fr/)
- [ ] Test contact and reservation forms
- [ ] Login to admin panel with admin/admin123456

### To Customize:
- [ ] Edit pages in admin panel
- [ ] Add menu items
- [ ] Upload images
- [ ] Change site settings (logo, contact info, social media)
- [ ] Create blog posts

### To Deploy (Later):
- Change to PostgreSQL database
- Set `DEBUG = False`
- Configure allowed hosts
- Setup email settings
- Use production WSGI server

---

## ENJOY! 🎉

Your restaurant website is ready to test. Start the server and explore!

**Questions?** Check the SETUP_COMPLETE.md file for detailed documentation.
