# Sip and SunShine Restaurant - Django Web Application

A fully-featured restaurant website built with Django, featuring multi-language support (English, Dutch, French), dynamic content management, and SEO optimization.

## Project Structure

```
sip-sunshine-django/
├── sip_sunshine/              # Project settings and configuration
│   ├── settings/              # Django settings
│   │   ├── base.py           # Base settings
│   │   └── development.py    # Development settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI application
├── restaurant/               # Main app
│   ├── models.py            # Database models
│   ├── views.py             # Views
│   ├── urls.py              # App URLs
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App config
│   └── migrations/          # Database migrations
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   └── pages/               # Page templates
├── static/                   # Static files
│   ├── css/                 # Stylesheets from Kusina template
│   ├── js/                  # JavaScript files
│   ├── images/              # Images
│   └── fonts/               # Fonts
├── media/                    # User-uploaded media
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── setup_db.py             # Database initialization script
```

## Features

### ✅ Implemented Features

1. **Dynamic Content Management**
   - Pages, Menu Items, Blog Posts, Content Blocks
   - All content managed from Django Admin Panel
   - CRUD operations for all content types

2. **Multi-Language Support**
   - English (Default), Dutch, French
   - Language switcher in navigation
   - All content translatable using django-parler
   - URL-based language switching

3. **SEO Management**
   - Meta titles, descriptions, and keywords per page
   - Translatable SEO settings
   - Sitemap support ready
   - Meta tags generation

4. **Site Management**
   - Global site settings (name, logo, contact info, social media)
   - Configurable contact information
   - Social media links
   - Google Maps embed support

5. **Core Pages**
   - Home Page with featured dishes and recent blogs
   - About Page with team section
   - Menu Page with categorized items
   - Blog Page with pagination
   - Blog Detail Page with related posts
   - Contact Page with form
   - Reservation Page with booking form

6. **Database Models**
   - **Page**: Website pages with SEO settings
   - **MenuItem**: Restaurant menu with categories and pricing
   - **BlogPost**: Blog articles with featured images
   - **ContentBlock**: Reusable content sections
   - **Reservation**: Booking requests
   - **ContactMessage**: Contact form submissions
   - **SiteSetting**: Global site configuration
   - **Language**: Language management

7. **Admin Panel**
   - Full admin interface for all models
   - Multi-language editing
   - Rich text support
   - Image upload functionality
   - Bulk actions

8. **Template Integration**
   - Uses Kusina restaurant template
   - Responsive Bootstrap design
   - All CSS, JS, and assets from original template
   - Owl Carousel, Magnific Popup, AOS animations

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual Environment (recommended)

### Step 1: Clone/Navigate to Project

```bash
cd f:\sunshine\sip-sunshine-django
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations

```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account credentials.

### Step 6: Initialize Database with Sample Data

```bash
python setup_db.py
```

This will:
- Create language records (English, Dutch, French)
- Create site settings
- Create pages (Home, About, Menu, Blog, Contact, Reservation)
- Create sample menu items in all languages

### Step 7: Static Assets

Static assets (CSS/JS/images/fonts) are already included in this repository under `static/`.
You do not need to copy assets from any external template folder.

### Step 8: Run Development Server

```bash
python manage.py runserver
```

The application will be available at:
- **Frontend**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## Usage Guide

### Accessing Admin Panel

1. Go to http://localhost:8000/admin/
2. Log in with your superuser credentials
3. Manage all content from the admin interface

### Managing Pages

1. Go to **Restaurant > Pages**
2. Create new pages or edit existing ones
3. Set page slug, title, content, and SEO settings
4. Translate content for each language
5. Mark as active/inactive

### Managing Menu Items

1. Go to **Restaurant > Menu Items**
2. Create items with name, price, category, and description
3. Upload images for items
4. Translate for all languages
5. Set order for display

### Managing Blog Posts

1. Go to **Restaurant > Blog Posts**
2. Create posts with title, excerpt, and full content
3. Upload featured image
4. Set publication date and status
5. Translate for all languages

### Managing Site Settings

1. Go to **Restaurant > Site Settings**
2. Update site name, logo, favicon
3. Configure contact information
4. Add social media URLs
5. Embed Google Maps

### Language Switching

**In Frontend:**
- Use the language dropdown in navigation bar
- Click your preferred language

**In Admin Panel:**
- Edit content in different languages using tabs
- Each language has its own fields

## API & URL Structure

### Frontend URLs

```
/                           - Home page
/en/                       - Home page (English)
/nl/                       - Home page (Dutch)
/fr/                       - Home page (French)
/menu/                     - Menu page
/about/                    - About page
/blog/                     - Blog listing
/blog/slug/                - Blog detail
/contact/                  - Contact page
/reservation/              - Reservation page
/admin/                    - Admin panel
```

### Language Prefix

All URLs automatically support language prefixes:
```
/en/menu/                  - English menu
/nl/menu/                  - Dutch menu
/fr/menu/                  - French menu
```

## Customization

### Adding New Pages

1. Create a page in admin: *Restaurant > Pages*
2. Choose template (or create new template in `templates/pages/`)
3. Add content and SEO settings
4. Translate for all languages

### Adding Menu Categories

Edit `restaurant/models.py` - `MenuItem.CATEGORY_CHOICES` and `MenuItemAdmin`

### Customizing Colors/Styling

Edit `static/css/style.css` or create custom CSS file

### Adding New Content Blocks

1. Edit `restaurant/models.py`
2. Create new `ContentBlock` types in `BLOCK_TYPE_CHOICES`
3. Update templates to use new blocks

## Database Models Guide

### Page
- `slug`: Unique URL identifier
- `template_name`: Which template to use
- `title`: Page title (translatable)
- `content`: Page content (translatable)
- `meta_title`: SEO title (translatable)
- `meta_description`: SEO description (translatable)
- `meta_keywords`: SEO keywords (translatable)

### MenuItem
- `category`: Food category (appetizers, main courses, etc.)
- `name`: Item name (translatable)
- `description`: Item description (translatable)
- `price`: Item price
- `image`: Optional item image
- `order`: Display order

### BlogPost
- `title`: Post title (translatable)
- `slug`: URL slug (translatable, unique per date)
- `author`: Author name
- `excerpt`: Short summary (translatable)
- `content`: Full content (translatable)
- `featured_image`: Header image
- `published_at`: Publication datetime
- `is_published`: Publication status

### ContentBlock
- `key`: Unique identifier (e.g., 'hero_home')
- `block_type`: Type of content block
- `title`: Block title (translatable)
- `content`: Block content (translatable)
- `image`: Block image
- `button_text`: CTA button text (translatable)
- `button_url`: Button link

### SiteSetting
- `site_name`: Website name
- `site_description`: Site description
- `site_logo`: Site logo image
- `email`: Contact email
- `phone`: Contact phone
- `address`: Restaurant address
- `facebook_url`: Facebook link
- `instagram_url`: Instagram link
- `twitter_url`: Twitter link
- `google_map_embed`: Embedded map HTML

## Important Notes

### Static Files in Development

Django automatically serves static files in development mode.

To collect static files for production:
```bash
python manage.py collectstatic --noinput
```

### Security Settings

⚠️ **IMPORTANT FOR PRODUCTION:**

1. Change `SECRET_KEY` in `sip_sunshine/settings/base.py`
2. Set `DEBUG = False` in production settings
3. Update `ALLOWED_HOSTS` with your domain
4. Use environment variables for sensitive data
5. Configure proper email settings for notifications

### Email Configuration

By default, emails are printed to console. To enable real email:

Edit `sip_sunshine/settings/base.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## Troubleshooting

### Database Issues
```bash
# Reset database completely
rm db.sqlite3
python manage.py migrate
python setup_db.py
```

### Missing Static Files
```bash
# Collect static files
python manage.py collectstatic
```

### Language Not Showing
- Check that languages are marked as active in admin
- Clear browser cache
- Ensure LANGUAGE_CODE is set correctly

### Template Issues
- Check template file exists in `templates/` folder
- Verify template name in Page model
- Check template syntax in browser console

## Next Steps

1. ✅ Test all pages and functionality locally
2. ✅ Customize colors and branding
3. ✅ Add your restaurant content
4. ✅ Test all languages
5. ✅ Upload images and media
6. ✅ Configure email settings
7. ✅ Test reservation and contact forms
8. After testing, create comprehensive documentation

## Support & Documentation

The project uses:
- **Django 4.2.7**: Web framework
- **django-parler**: Multi-language support
- **Bootstrap**: CSS framework
- **Kusina Template**: Responsive design

For more information:
- Django Docs: https://docs.djangoproject.com/
- django-parler: https://django-parler.readthedocs.io/
- Bootstrap: https://getbootstrap.com/

## Created By

Sip and SunShine Restaurant Django Project
Built with Django, featuring dynamic content management and multi-language support.

---

**Ready to go live?** Test thoroughly in the local system first, then we'll prepare production deployment documentation.
