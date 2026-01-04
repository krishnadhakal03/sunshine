# Language Testing & Implementation Guide

## Quick Start - Test Multi-Language Support

### Prerequisites
- Django running on `http://localhost:2005`
- Admin credentials: `admin / admin123456`

---

## Testing Languages

### Test URLs

1. **English Version**
   ```
   http://localhost:2005/en/
   http://localhost:2005/en/menu/
   http://localhost:2005/en/contact/
   http://localhost:2005/en/reservation/
   ```

2. **Dutch Version**
   ```
   http://localhost:2005/nl/
   http://localhost:2005/nl/menu/
   http://localhost:2005/nl/contact/
   http://localhost:2005/nl/reservation/
   ```

3. **French Version**
   ```
   http://localhost:2005/fr/
   http://localhost:2005/fr/menu/
   http://localhost:2005/fr/contact/
   http://localhost:2005/fr/reservation/
   ```

---

## Language Switcher Testing

### Using Frontend Language Switcher
1. Visit any page: `http://localhost:2005/`
2. Look for **language selector** in the top navigation
3. Click on language option (English, Français, Nederlands)
4. Page should reload in that language
5. All text should update accordingly

### What Should Translate
- ✅ Navigation menu items
- ✅ Page titles and headings
- ✅ Form labels and placeholders
- ✅ Button text
- ✅ Section headers
- ✅ Menu categories
- ✅ Days of week (Monday, Tuesday, etc.)
- ✅ All static text

---

## Admin Interface Translation

### Step 1: Login to Admin
```
URL: http://localhost:2005/admin/
Username: admin
Password: admin123456
```

### Step 2: Navigate to Models

#### Option A: Translate Menu Items
1. Go to **Restaurant > Menu Items**
2. Click on any menu item (e.g., "Bruschetta")
3. You'll see **3 language tabs** at the top:
   - **English**
   - **Dutch (Nederlands)**
   - **Français (French)**

4. Click each tab and update:
   - **Name**: Item name in that language
   - **Description**: Item description in that language

5. Click **Save**

**Example Translations:**
- English: "Bruschetta" → Dutch: "Bruchetta" → French: "Bruschetta"
- English: "Crispy bread with tomato & garlic" → Dutch: "Knapperig brood met tomaat en knoflook" → French: "Pain croustillant avec tomate et ail"

#### Option B: Translate Pages
1. Go to **Restaurant > Pages**
2. Click on a page (e.g., "About")
3. Use language tabs to edit:
   - **Title**
   - **Meta Title** (SEO)
   - **Content** (main text)

4. Save after each language

#### Option C: Translate Blog Posts
1. Go to **Restaurant > Blog Posts**
2. Click on a post
3. Use language tabs to edit:
   - **Title**
   - **Content**
4. Save

---

## Checking Translations

### Test Each Page in All Languages

#### Home Page Checklist
- [ ] Hero section headings display correctly
- [ ] Menu category names show in correct language
- [ ] "Book A Table" button translates
- [ ] "Featured Dishes" section title translates
- [ ] "View Full Menu" button translates

#### Menu Page Checklist
- [ ] Page title shows "Menu - Specialties" in correct language
- [ ] All menu category buttons translate (Appetizers, Main Courses, etc.)
- [ ] Menu item names display from database
- [ ] "Add to Order" button translates

#### Reservation Page Checklist
- [ ] "Book A Table" heading appears correctly
- [ ] Form labels all translate (Name, Email, Phone, etc.)
- [ ] Form placeholders show in correct language
- [ ] "Reserve Now" button translates
- [ ] Opening hours display days of week in correct language

#### Contact Page Checklist
- [ ] "Contact Us" heading translates
- [ ] Form labels translate (Name, Email, Subject, Message)
- [ ] Form placeholders in correct language
- [ ] "Send Message" button translates
- [ ] Contact info cards show correct language (Address, Phone, Email)

---

## Troubleshooting

### If Text Doesn't Translate

#### Problem: Page shows English even after clicking Dutch
**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh the page (Ctrl+F5)
3. Try accessing with URL directly: `http://localhost:2005/nl/menu/`

#### Problem: Django Admin shows only English
**Solution:**
1. Make sure database is populated
2. Run: `python setup_db.py`
3. Then refresh admin page

#### Problem: Menu items don't show translations
**Solution:**
1. Go to admin panel
2. Edit menu item using language tabs
3. Make sure you're in the correct language tab
4. Save changes
5. Clear cache and refresh

---

## Database Translation Storage

### How It Works
- Translations are stored in separate database tables
- When you view a page, Django fetches the correct language
- Fallback to English if translation missing

### Translation Tables Created by django-parler:
- `restaurant_menuitem_translations`
- `restaurant_page_translations`
- `restaurant_blogpost_translations`
- `restaurant_contentblock_translations`

---

## Backend Code Implementation

### All Pages Already Have:

#### Templates with {% load i18n %}
- ✅ `base.html` - Navigation, footer, shared elements
- ✅ `pages/index.html` - Home page (ALL text translated)
- ✅ `pages/menu.html` - Menu page (ALL text translated)
- ✅ `pages/contact.html` - Contact page (ALL text translated)
- ✅ `pages/reservation.html` - Reservation page (ALL text translated)

#### Models with TranslatableModel
- ✅ `MenuItem` - Menu items
- ✅ `Page` - Website pages
- ✅ `BlogPost` - Blog articles
- ✅ `ContentBlock` - Custom content

#### Settings Configured
- ✅ Language codes: EN, NL, FR
- ✅ i18n middleware installed
- ✅ Parler language configuration
- ✅ Default fallback language: English

---

## Language Codes

| Language | Code | Django Name |
|----------|------|-------------|
| English | `en` | English |
| Dutch | `nl` | Dutch (Nederlands) |
| French | `fr` | Français |

---

## Common Questions

### Q: How do I add a new language?
A: Edit `sip_sunshine/settings/base.py`:
```python
LANGUAGES = [
    ('en', 'English'),
    ('nl', 'Dutch'),
    ('fr', 'French'),
    ('de', 'German'),  # Add new language
]
```
Then: `python manage.py makemessages -l de`

### Q: How do I translate Python code strings?
A: Use `gettext_lazy`:
```python
from django.utils.translation import gettext_lazy as _

category_choices = [
    ('appetizers', _('Appetizers')),  # This will translate
]
```

### Q: Will dynamic content translate?
A: Yes! Content from admin interface (Menu Items, Pages, Blog) automatically translates via language tabs in admin panel.

### Q: What if a translation is missing?
A: Falls back to English (default) or original language string.

---

## Performance Notes

- Translations are cached for better performance
- First request in a language may be slower (cache miss)
- Subsequent requests fast (cache hit)
- Cache clears on Django restart

---

## Next Steps for Production

1. **Generate .po files** (if needed):
   ```bash
   python manage.py makemessages -l nl
   python manage.py makemessages -l fr
   python manage.py compilemessages
   ```

2. **Fill in admin translations** via Django Admin panel
   - Translate menu items
   - Translate page content
   - Translate blog posts

3. **Set default language** in settings
   ```python
   LANGUAGE_CODE = 'en'  # Default when no language selected
   ```

4. **Test all languages** before going live

5. **Deploy** - translations go with you!

---

## Support Resources

- Django i18n docs: https://docs.djangoproject.com/en/4.2/topics/i18n/
- django-parler docs: https://github.com/django-parler/django-parler
- Translation management: `/admin/restaurant/language/`

---

**Translation System Ready!** ✅

All pages support English, Dutch, and French. Users can switch languages from the website header.

