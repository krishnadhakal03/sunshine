# Translation Guide - Multi-Language Support

## Overview
The Sip and Sunshine website supports **3 languages**:
- 🇬🇧 **English** (en)
- 🇳🇱 **Dutch/Nederlands** (nl)
- 🇫🇷 **French/Français** (fr)

## Configuration

### Settings (sip_sunshine/settings/base.py)
```python
LANGUAGE_CODE = 'en'  # Default language
LANGUAGES = [
    ('en', 'English'),
    ('nl', 'Dutch (Nederlands)'),
    ('fr', 'French (Français)'),
]
USE_I18N = True
PARLER_LANGUAGES = {
    None: (
        {'code': 'en', 'name': 'English'},
        {'code': 'nl', 'name': 'Dutch'},
        {'code': 'fr', 'name': 'French'},
    ),
    'default': {
        'fallbacks': ['en']
    }
}
```

## Translation System

### 1. **Models** (django-parler)
Models use `TranslatableModel` and `TranslatedFields`:

```python
from parler.models import TranslatableModel, TranslatedFields

class MenuItem(TranslatableModel):
    price = models.DecimalField(max_digits=6, decimal_places=2)
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        description=models.TextField(),
    )
```

**Available Translatable Models:**
- `MenuItem` - Menu items with translations for name, description
- `Page` - Website pages (About, Home, etc.)
- `BlogPost` - Blog articles
- `ContentBlock` - Custom content blocks

### 2. **Templates** (Django i18n template tags)

#### Load translation tags
```django
{% load i18n %}
```

#### Translate static strings
```django
{% trans "Hello World" %}
```

#### Translate blocks with context
```django
{% blocktrans %}This is a longer message{% endblocktrans %}
```

#### Translate with variables
```django
{% blocktrans with name="John" %}Hello {{ name }}{% endblocktrans %}
```

### 3. **Python Code** (gettext_lazy)

```python
from django.utils.translation import gettext_lazy as _

class MenuItem(models.Model):
    category = models.CharField(
        max_length=20,
        choices=[
            ('appetizers', _('Appetizers')),
            ('main_courses', _('Main Courses')),
            ('desserts', _('Desserts')),
        ]
    )
```

## Pages with Translations

### ✅ Implemented Translations

#### Home Page (index.html)
- Hero sections (all headings and descriptions)
- Menu categories (Fresh Appetizers, Main Courses, Desserts, Fine Wines, Cocktails)
- Featured Dishes section
- Blog section ("Recent Stories")
- Call-to-action buttons

#### Menu Page (menu.html)
- Page title and hero section
- Menu category buttons (Appetizers, Breakfast, Main Courses, BBQ, Desserts, Beverages, Cocktails)
- Menu descriptions
- "No items available" messages

#### Reservation Page (reservation.html)
- Page title and hero section
- Form labels (Name, Email, Phone, Date, Time, Guests, Special Requests)
- Form placeholders
- Submit button
- Opening hours section

#### Contact Page (contact.html)
- Page title and hero section
- Contact form title and labels
- Form fields (Name, Email, Phone, Subject, Message)
- Contact information cards (Address, Phone, Email)
- Section titles and descriptions

#### Base Template (base.html)
- Navigation menu items (Home, About, Menu, Blog, Contact, Reservation)
- Open Hours section
- Footer links
- Days of week (Monday - Sunday)

### Database Models with Translations
- **MenuItem** - name, description
- **Page** - title, meta_title, slug, content
- **BlogPost** - title, slug, content
- **ContentBlock** - title, content

## How to Add/Update Translations

### Option 1: Django Admin Interface

1. Go to `http://localhost:2005/admin/`
2. Navigate to **Menu Items**, **Pages**, or **Blog Posts**
3. Click on an item to edit
4. Use the **language selector** at the top to switch languages
5. Edit the translated fields
6. Save

**Language selector shows**: English, Dutch (Nederlands), French (Français)

### Option 2: Management Command (For bulk translations)

To extract all translatable strings:
```bash
python manage.py makemessages -l nl  # Dutch
python manage.py makemessages -l fr  # French
python manage.py compilemessages
```

## Language Switcher

The website provides a language switcher in the header. Users can:
1. Click on the language dropdown
2. Select English, Dutch, or French
3. Page will reload in selected language

Language buttons are generated from the database (`Language` model):
```html
{% for lang in active_languages %}
    <a href="/?lang={{ lang.code }}">{{ lang.name }}</a>
{% endfor %}
```

## URL Language Prefix

Enable URL language prefixes in `settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    ...
]
```

URLs will then be:
- English: `http://localhost:2005/en/menu/`
- Dutch: `http://localhost:2005/nl/menu/`
- French: `http://localhost:2005/fr/menu/`

## Testing Translations

### Test Home Page
```bash
# English
http://localhost:2005/en/

# Dutch
http://localhost:2005/nl/

# French
http://localhost:2005/fr/
```

### Test Menu Categories
- All buttons should display in correct language
- Click categories to navigate to correct menu section

### Test Admin Interface
- Go to `/admin/restaurant/menuitem/`
- Edit a menu item
- Switch language tabs to view/edit Dutch and French translations

## Translation Checklist

- [x] Navigation menu items
- [x] Home page hero sections
- [x] Menu categories
- [x] Featured dishes section
- [x] Blog section
- [x] Reservation form
- [x] Contact form
- [x] Contact information cards
- [x] Opening hours
- [x] Footer links
- [x] Menu items names/descriptions (via admin)
- [x] Page titles and content (via admin)
- [x] Blog posts (via admin)

## Common Translation Strings

| English | Dutch | French |
|---------|-------|--------|
| Fresh Appetizers | Verse Voorgerechten | Frais Appétitifs |
| Main Courses | Hoofdgerechten | Plats Principaux |
| Desserts | Desserts | Desserts |
| Beverages | Dranken | Boissons |
| Cocktails | Cocktails | Cocktails |
| Breakfast | Ontbijt | Petit-déjeuner |
| Book A Table | Tafel Reserveren | Réserver une Table |
| Reserve Now | Nu Reserveren | Réserver Maintenant |
| Contact Us | Neem Contact Op | Contactez-Nous |

## Frontend Language Detection

The template uses `{{ LANGUAGE_CODE }}` to:
- Set the HTML `lang` attribute: `<html lang="{{ LANGUAGE_CODE }}">`
- Pass to JavaScript for locale-specific formatting
- Display the current active language

## Notes

- Default fallback is **English** if translation is missing
- All user content (menu items, pages, blog posts) can be translated via Django Admin
- Template strings are translated via `{% trans %}` tags
- Database models use django-parler for multi-language support
- Translations are cached - restart Django after makemessages/compilemessages
