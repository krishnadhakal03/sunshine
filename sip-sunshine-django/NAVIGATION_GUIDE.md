# 🗺️ Navigation Guide - Where to Find What

## 📚 Start Here

### First Time? Read These (In Order)

1. **PROJECT_SUMMARY.md** - Quick overview of what was built
2. **QUICKSTART.md** - How to set up and run
3. **This file** - Where to find things

---

## 🎯 Common Tasks & Files

### ❓ "I want to understand the project structure"
→ Read: **FILE_INDEX.md**  
→ Or: **README.md**

### ❓ "How do I get this running?"
→ Read: **QUICKSTART.md**  
→ Run: `quickstart.bat` (Windows) or `bash quickstart.sh` (Mac/Linux)

### ❓ "How do I add a new page?"
→ Read: **README.md** → Customization section  
→ Create: New Page in admin panel  
→ Create: New template in `templates/pages/`  
→ Edit: `restaurant/urls.py` if needed

### ❓ "How do I add menu items?"
→ Go to: Admin panel → Restaurant → Menu Items  
→ Or read: **README.md** → Usage Guide

### ❓ "How do I change site name/logo?"
→ Go to: Admin panel → Restaurant → Site Settings  
→ Or read: **README.md** → Managing Site Settings

### ❓ "How do I add a language?"
→ Edit: `restaurant/models.py` → Language model  
→ Or read: **README.md** → Multi-language Support

### ❓ "The website doesn't look styled"
→ Do: Copy CSS/JS files from Kusina  
→ Read: **TEMPLATE_ASSETS_INTEGRATION.md**

### ❓ "I need to copy the template assets"
→ Read: **TEMPLATE_ASSETS_INTEGRATION.md**  
→ Follow all steps exactly

### ❓ "I want to see what models exist"
→ Read: `restaurant/models.py`  
→ Or read: **FILE_INDEX.md** → Database Models

### ❓ "I want to customize the styling"
→ Edit: `static/css/style.css`  
→ Or edit templates in: `templates/`

### ❓ "Something's not working"
→ Read: **README.md** → Troubleshooting  
→ Or read: **QUICKSTART.md** → Common Issues

### ❓ "What files do I need to change?"
→ Rarely needed! Most changes via admin panel.  
→ To add features, read: **README.md** → Customization

---

## 🗂️ File Organization Quick Reference

```
PROJECT ROOT: f:\sunshine\sip-sunshine-django\
│
├─ 📚 DOCUMENTATION (Read these)
│  ├─ README.md                        ← FULL DOCUMENTATION
│  ├─ QUICKSTART.md                    ← HOW TO RUN
│  ├─ PROJECT_SUMMARY.md               ← OVERVIEW
│  ├─ PROJECT_COMPLETION_STATUS.md     ← WHAT'S DONE
│  ├─ FILE_INDEX.md                    ← FILE REFERENCE
│  ├─ TEMPLATE_ASSETS_INTEGRATION.md   ← HOW TO COPY ASSETS
│  └─ NAVIGATION_GUIDE.md              ← THIS FILE
│
├─ 🐍 PYTHON CODE (Modify if needed)
│  ├─ sip_sunshine/settings/base.py    ← Django settings
│  ├─ sip_sunshine/settings/development.py ← Dev settings
│  ├─ sip_sunshine/urls.py             ← Main URL config
│  ├─ restaurant/models.py             ← Database models
│  ├─ restaurant/views.py              ← Page logic
│  ├─ restaurant/urls.py               ← App URLs
│  ├─ restaurant/admin.py              ← Admin interface
│  └─ restaurant/context_processors.py ← Template helpers
│
├─ 🎨 TEMPLATES (Modify for custom pages)
│  ├─ templates/base.html              ← Base template
│  └─ templates/pages/
│     ├─ index.html                    ← Homepage
│     ├─ about.html                    ← About
│     ├─ menu.html                     ← Menu
│     ├─ blog.html                     ← Blog list
│     ├─ blog-single.html              ← Blog detail
│     ├─ contact.html                  ← Contact
│     ├─ reservation.html              ← Reservation
│     └─ page.html                     ← Generic page
│
├─ 📁 STATIC (Copy from Kusina)
│  ├─ static/css/                      ← CSS files
│  ├─ static/js/                       ← JavaScript files
│  ├─ static/images/                   ← Images
│  └─ static/fonts/                    ← Fonts
│
├─ 📤 MEDIA (User uploads)
│  └─ media/                           ← Images, files
│
├─ 🔧 SCRIPTS & CONFIG
│  ├─ manage.py                        ← Django CLI
│  ├─ requirements.txt                 ← Dependencies
│  ├─ setup_db.py                      ← Initialize DB
│  ├─ quickstart.bat                   ← Windows setup
│  └─ quickstart.sh                    ← Linux/Mac setup
│
└─ 💾 DATABASE (Created when running)
   └─ db.sqlite3                       ← SQLite database
```

---

## 🎯 Quick Find By Purpose

### I Want To...

| Goal | File to Edit | Or | Admin Panel |
|------|-------------|----|----|
| Change site name/logo | settings | Admin → Site Settings | ✅ EASIER |
| Add a page | templates/pages/ | Page model | ✅ EASIER |
| Add menu item | - | Menu Item model | ✅ EASIER |
| Write blog post | - | Blog Post model | ✅ EASIER |
| Change colors | static/css/style.css | - | ❌ Need CSS |
| Add content block | - | Content Block model | ✅ EASIER |
| Change footer | templates/base.html | - | ❌ Need HTML |
| Change navbar | templates/base.html | - | ❌ Need HTML |
| Add new language | models.py | Language model | 🟡 BOTH |
| Configure email | settings/base.py | - | ❌ Need Python |
| Add reservations | models.py | Already exists! | ✅ READY |
| View form submissions | - | Admin panel | ✅ READY |

---

## 🔍 Finding Things In Code

### Location of Database Models
**File**: `restaurant/models.py`

```python
class Page(TranslatableModel):        # Homepage, About, Menu, etc.
class MenuItem(TranslatableModel):    # Menu items with prices
class BlogPost(TranslatableModel):    # Blog articles
class ContentBlock(TranslatableModel):# Reusable sections
class Reservation(models.Model):      # Booking requests
class ContactMessage(models.Model):   # Contact forms
class SiteSetting(models.Model):      # Site configuration
class Language(models.Model):         # Languages (EN, NL, FR)
```

### Location of Views
**File**: `restaurant/views.py`

```python
class HomePageView:                   # Homepage
class AboutPageView:                  # About page
class MenuPageView:                   # Menu page
class BlogListView:                   # Blog listing
class BlogDetailView:                 # Single blog post
class ContactView:                    # Contact page & form
class ReservationView:                # Reservation page & form
class PageView:                       # Generic pages
```

### Location of Templates
**Directory**: `templates/pages/`

```
index.html              → Homepage
about.html              → About page
menu.html               → Menu page
blog.html               → Blog listing
blog-single.html        → Blog detail
contact.html            → Contact & form
reservation.html        → Reservation & form
page.html               → Generic page
base.html               → Base (nav, footer)
```

### Location of Settings
**File**: `sip_sunshine/settings/base.py`

- INSTALLED_APPS → Which apps are active
- DATABASES → Database configuration
- LANGUAGES → Language settings
- STATIC_URL → CSS/JS location
- MEDIA_ROOT → Uploads location
- EMAIL_BACKEND → Email settings

### Location of Admin Config
**File**: `restaurant/admin.py`

```python
LanguageAdmin           → Manage languages
SiteSettingAdmin        → Configure site
PageAdmin               → Manage pages
MenuItemAdmin           → Manage menu items
ContentBlockAdmin       → Manage content blocks
BlogPostAdmin           → Manage blog posts
ReservationAdmin        → View reservations
ContactMessageAdmin     → View messages
```

### Location of URLs
**File**: `restaurant/urls.py`

```python
# All URLs with language prefixes:
/                       → Home
/en/menu/               → English menu
/nl/menu/               → Dutch menu
/fr/menu/               → French menu
/about/                 → About
/blog/                  → Blog
/blog/<slug>/           → Blog detail
/contact/               → Contact
/reservation/           → Reservation
/admin/                 → Admin
```

---

## 📱 Testing Paths

### Test Each Feature At:

1. **Homepage**
   - URL: http://localhost:8000/
   - Check: Featured items, blog, styling

2. **Menu Page**
   - URL: http://localhost:8000/menu/
   - Check: Categories, prices, images

3. **Blog Page**
   - URL: http://localhost:8000/blog/
   - Check: Posts, pagination, images

4. **Blog Detail**
   - URL: http://localhost:8000/blog/post-slug/
   - Check: Full article, related posts

5. **About Page**
   - URL: http://localhost:8000/about/
   - Check: Team section, content

6. **Contact Page**
   - URL: http://localhost:8000/contact/
   - Check: Form, map, info

7. **Reservation Page**
   - URL: http://localhost:8000/reservation/
   - Check: Form, hours

8. **Language Switching**
   - URL: http://localhost:8000/nl/
   - Check: Content in Dutch
   - URL: http://localhost:8000/fr/
   - Check: Content in French

9. **Admin Panel**
   - URL: http://localhost:8000/admin/
   - Check: All models visible

10. **Forms**
    - Contact: Submit test message
    - Check: Admin → Contact Messages
    - Reservation: Submit test booking
    - Check: Admin → Reservations

---

## 🚀 Common Workflows

### Workflow: Add a New Menu Item

1. Go to: Admin → Restaurant → Menu Items
2. Click: "Add Menu Item"
3. Fill:
   - Category: Choose one
   - Price: Enter price
   - Image: Upload image
4. Click: "Save and Continue Editing"
5. Switch to: Dutch tab
6. Fill: Name (Dutch) and Description (Dutch)
7. Click: "Save"
8. Repeat for French if needed
9. Visit: http://localhost:8000/menu/

### Workflow: Create a Blog Post

1. Go to: Admin → Restaurant → Blog Posts
2. Click: "Add Blog Post"
3. Fill:
   - Title: Post title
   - Slug: URL slug
   - Author: Your name
   - Excerpt: Summary
   - Content: Full text
   - Featured Image: Upload image
4. Translate: Switch tabs for other languages
5. Publish: Check "Is Published" and set date
6. Save
7. Visit: http://localhost:8000/blog/

### Workflow: Change Site Name

1. Go to: Admin → Restaurant → Site Settings
2. Edit: "Site Name" field
3. Save
4. Navbar now shows new name

### Workflow: Copy Template Assets

1. Read: TEMPLATE_ASSETS_INTEGRATION.md
2. Run commands for your OS
3. Restart Django server
4. Visit: Homepage should be styled

---

## ❓ FAQ & File Locations

**Q: Where is the homepage?**  
A: `templates/pages/index.html` or `restaurant/views.py` (HomePageView)

**Q: Where is the menu page?**  
A: `templates/pages/menu.html` or `restaurant/views.py` (MenuPageView)

**Q: Where is the database?**  
A: `db.sqlite3` (created after first migration)

**Q: Where do I add a new page?**  
A: Admin panel → Pages (OR `templates/pages/` for template)

**Q: Where do I configure email?**  
A: `sip_sunshine/settings/base.py` → EMAIL_* settings

**Q: Where are the CSS files?**  
A: `static/css/` (after copying from Kusina)

**Q: Where are the JavaScript files?**  
A: `static/js/` (after copying from Kusina)

**Q: Where are uploaded images?**  
A: `media/` folder

**Q: Where is the admin interface config?**  
A: `restaurant/admin.py`

**Q: Where are the database models?**  
A: `restaurant/models.py`

**Q: Where are the views/logic?**  
A: `restaurant/views.py`

**Q: Where are the URLs?**  
A: `restaurant/urls.py`

**Q: Where are the settings?**  
A: `sip_sunshine/settings/`

---

## 🔑 Key Files to Understand

### Must Read First
1. **README.md** - Everything explained
2. **QUICKSTART.md** - How to run

### To Understand Architecture
1. **restaurant/models.py** - Data structure
2. **restaurant/views.py** - Logic
3. **restaurant/urls.py** - Routing
4. **restaurant/admin.py** - Admin

### To Customize
1. **templates/base.html** - Common elements
2. **templates/pages/*.html** - Page content
3. **static/css/style.css** - Styling
4. **sip_sunshine/settings/base.py** - Configuration

---

## 💡 Pro Tips

✨ **Most changes through admin panel** - Don't modify code unless needed

✨ **Backup before major changes** - Copy db.sqlite3 before testing

✨ **Use browser inspector** - F12 to debug CSS/JS issues

✨ **Check server output** - Terminal shows errors during development

✨ **Read the comments** - Code has helpful comments

✨ **Test language switching** - Make sure everything translates

---

## 🎓 Learning Resources

**Django Official Docs**: https://docs.djangoproject.com/  
**django-parler Docs**: https://django-parler.readthedocs.io/  
**Bootstrap Docs**: https://getbootstrap.com/docs/

---

**Everything is organized and documented!**  
**Pick what you want to do and find the corresponding file.** 🚀
