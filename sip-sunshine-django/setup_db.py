"""
Quick setup script for Sip and SunShine Django project
Run this after initial setup to populate the database with sample data
"""

import os
import django
from django.utils import timezone
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip_sunshine.settings.development')
django.setup()

from restaurant.models import Language, SiteSetting, Page, MenuItem, ContentBlock, BlogPost
from django.utils.translation import activate


def setup_database():
    """Setup initial database content"""
    
    print("=" * 60)
    print("Setting up Sip and SunShine Restaurant Database")
    print("=" * 60)
    
    # 1. Ensure languages exist
    print("\n[LANGUAGES] Setting up languages...")
    languages = [
        {'code': 'en', 'name': 'English', 'is_default': True},
        {'code': 'nl', 'name': 'Dutch (Nederlands)', 'is_default': False},
        {'code': 'fr', 'name': 'French (Francais)', 'is_default': False},
    ]
    
    for lang in languages:
        obj, created = Language.objects.get_or_create(
            code=lang['code'],
            defaults={'name': lang['name'], 'is_default': lang['is_default']}
        )
        status = "Created" if created else "Already exists"
        print(f"  - {lang['name']}: {status}")
    
    # 2. Setup Site Settings
    print("\n[SETTINGS] Setting up site settings...")
    site_settings, created = SiteSetting.objects.get_or_create(
        id=1,
        defaults={
            'site_name': 'Sip and SunShine',
            'site_description': 'Welcome to Sip and SunShine - Your premier Belgian restaurant specializing in breakfast, BBQ, and craft drinks. Experience authentic flavors in a warm, welcoming atmosphere.',
            'site_keywords': 'restaurant, Belgian food, breakfast, BBQ, drinks, cocktails, dining, Amsterdam',
            'email': 'info@sipandsunshine.com',
            'phone': '+31 (0)20 123 4567',
            'address': '45 Prinsengracht, 1015 DK Amsterdam, Netherlands',
            'facebook_url': 'https://facebook.com/sipandsunshine',
            'instagram_url': 'https://instagram.com/sipandsunshine',
            'twitter_url': 'https://twitter.com/sipandsunshine',
            'google_map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2436.5217395895267!2d4.884165!3d52.370216!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47c5c9e9c9e9c9eb%3A0x1234567890ab!2s45%20Prinsengracht%2C%201015%20DK%20Amsterdam!5e0!3m2!1sen!2snl!4v1234567890123" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>',
        }
    )
    status = "Created" if created else "Already exists"
    print(f"  - Site settings: {status}")
    if not created:
        # Update existing with new dummy data
        site_settings.site_description = 'Welcome to Sip and SunShine - Your premier Belgian restaurant specializing in breakfast, BBQ, and craft drinks. Experience authentic flavors in a warm, welcoming atmosphere.'
        site_settings.phone = '+31 (0)20 123 4567'
        site_settings.address = '45 Prinsengracht, 1015 DK Amsterdam, Netherlands'
        site_settings.google_map_embed = '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2436.5217395895267!2d4.884165!3d52.370216!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47c5c9e9c9e9c9eb%3A0x1234567890ab!2s45%20Prinsengracht%2C%201015%20DK%20Amsterdam!5e0!3m2!1sen!2snl!4v1234567890123" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
        site_settings.save()
        print(f"  - Site settings: Updated with new dummy data")
    
    # 3. Create Pages
    print("\n[PAGES] Creating pages...")
    pages_data = [
        {
            'slug': 'home',
            'template_name': 'index',
            'is_homepage': True,
            'order': 1,
            'titles': {'en': 'Home', 'nl': 'Thuis', 'fr': 'Accueil'},
            'meta_titles': {'en': 'Sip and SunShine - Home', 'nl': 'Sip and SunShine - Thuis', 'fr': 'Sip and SunShine - Accueil'},
        },
        {
            'slug': 'about',
            'template_name': 'about',
            'order': 2,
            'titles': {'en': 'About Us', 'nl': 'Over Ons', 'fr': 'À Propos'},
            'meta_titles': {'en': 'About Sip and SunShine', 'nl': 'Over Sip and SunShine', 'fr': 'À Propos de Sip and SunShine'},
        },
        {
            'slug': 'menu',
            'template_name': 'menu',
            'order': 3,
            'titles': {'en': 'Menu', 'nl': 'Menu', 'fr': 'Menu'},
            'meta_titles': {'en': 'Our Menu', 'nl': 'Ons Menu', 'fr': 'Notre Menu'},
        },
        {
            'slug': 'blog',
            'template_name': 'blog',
            'order': 4,
            'titles': {'en': 'Blog', 'nl': 'Blog', 'fr': 'Blog'},
            'meta_titles': {'en': 'Blog', 'nl': 'Blog', 'fr': 'Blog'},
        },
        {
            'slug': 'contact',
            'template_name': 'contact',
            'order': 5,
            'titles': {'en': 'Contact', 'nl': 'Contact', 'fr': 'Contact'},
            'meta_titles': {'en': 'Contact Us', 'nl': 'Contact Ons', 'fr': 'Nous Contacter'},
        },
        {
            'slug': 'reservation',
            'template_name': 'reservation',
            'order': 6,
            'titles': {'en': 'Reservation', 'nl': 'Reservering', 'fr': 'Réservation'},
            'meta_titles': {'en': 'Make a Reservation', 'nl': 'Maak een Reservering', 'fr': 'Faire une Réservation'},
        },
    ]
    
    for page_data in pages_data:
        page, created = Page.objects.get_or_create(
            slug=page_data['slug'],
            defaults={
                'template_name': page_data['template_name'],
                'is_homepage': page_data.get('is_homepage', False),
                'order': page_data['order'],
            }
        )
        
        # Set translations
        for lang_code, title in page_data['titles'].items():
            activate(lang_code)
            page.set_current_language(lang_code)
            page.title = title
            page.meta_title = page_data['meta_titles'].get(lang_code, '')
            page.save()
        
        print(f"  - {page_data['slug']}: {'Created' if created else 'Already exists'}")
    
    # 4. Create Menu Items
    print("\n✓ Creating menu items...")
    menu_items = [
        # Appetizers - Belgian Style
        {
            'category': 'appetizers',
            'price': '7.50',
            'names': {'en': 'Croquettes aux Crevettes', 'nl': 'Garnalenkroketten', 'fr': 'Croquettes aux Crevettes'},
            'descriptions': {'en': 'Belgian shrimp croquettes with chipotle mayo', 'nl': 'Belgische garnalenkroketten met chipolimayonaise', 'fr': 'Croquettes de crevettes belges avec mayo chipotle'},
        },
        {
            'category': 'appetizers',
            'price': '6.50',
            'names': {'en': 'Mussels & Fries', 'nl': 'Mosselen & Patat', 'fr': 'Moules & Frites'},
            'descriptions': {'en': 'Steamed mussels in white wine with Belgian fries', 'nl': 'Gestoomde mosselen in witte wijn met Belgische friet', 'fr': 'Moules à la vapeur en vin blanc avec frites belges'},
        },
        {
            'category': 'appetizers',
            'price': '8.00',
            'names': {'en': 'Cheese Croquettes', 'nl': 'Kaaskroketten', 'fr': 'Croquettes au Fromage'},
            'descriptions': {'en': 'Golden fried croquettes with Emmental and Gouda', 'nl': 'Goudkleurig gebakken kroketten met Emmental en Gouda', 'fr': 'Croquettes dorées à la friture avec Emmental et Gouda'},
        },
        {
            'category': 'appetizers',
            'price': '9.00',
            'names': {'en': 'Waterzooi Velouté', 'nl': 'Waterzooi Velouté', 'fr': 'Velouté Waterzooi'},
            'descriptions': {'en': 'Creamy Flemish vegetable soup with chicken', 'nl': 'Romige Vlaamse groentesop met kip', 'fr': 'Soupe de légumes flamande crémeuse avec poulet'},
        },
        # Main Courses - Belgian Style
        {
            'category': 'main_courses',
            'price': '16.50',
            'names': {'en': 'Moules Frites', 'nl': 'Mosselen met Friet', 'fr': 'Moules Frites'},
            'descriptions': {'en': 'Fresh mussels steamed in white wine, garlic & herbs with Belgian fries', 'nl': 'Verse mosselen gestoomd in witte wijn, knoflook & kruiden met Belgische friet', 'fr': 'Moules fraîches cuites à la vapeur en vin blanc, ail & herbes avec frites belges'},
        },
        {
            'category': 'main_courses',
            'price': '18.00',
            'names': {'en': 'Carbonnade Flamande', 'nl': 'Carbonnade Flamande', 'fr': 'Carbonnade Flamande'},
            'descriptions': {'en': 'Slow-cooked beef in Belgian beer with Belgian fries', 'nl': 'Langzaam gestoofd rundvlees in Belgisch bier met Belgische friet', 'fr': 'Boeuf braisé à la bière belge avec frites belges'},
        },
        {
            'category': 'main_courses',
            'price': '19.50',
            'names': {'en': 'Stoemp & Sausage', 'nl': 'Stoemp & Worst', 'fr': 'Stoemp & Saucisse'},
            'descriptions': {'en': 'Mashed potatoes with vegetables and Belgian sausage', 'nl': 'Aardappelpuree met groenten en Belgische worst', 'fr': 'Purée de pommes de terre avec légumes et saucisse belge'},
        },
        {
            'category': 'main_courses',
            'price': '20.00',
            'names': {'en': 'Pan-Fried Chicken Waterzooi', 'nl': 'Gebakken Kip Waterzooi', 'fr': 'Poulet Poêlé Waterzooi'},
            'descriptions': {'en': 'Belgian-style creamy chicken stew with vegetables', 'nl': 'Belgische romige kipstoof met groenten', 'fr': 'Ragoût de poulet crémeuse à la belge avec légumes'},
        },
        {
            'category': 'main_courses',
            'price': '22.00',
            'names': {'en': 'Wild Boar Stew', 'nl': 'Wildbraadschotel', 'fr': 'Ragoût de Sanglier'},
            'descriptions': {'en': 'Tender wild boar with mushrooms and beer reduction', 'nl': 'Mals wildbraad met paddenstoelen en bierreductie', 'fr': 'Sanglier tendre avec champignons et réduction à la bière'},
        },
        {
            'category': 'main_courses',
            'price': '21.00',
            'names': {'en': 'North Sea Sole Meunière', 'nl': 'Tong à la Meunière', 'fr': 'Sole de Mer du Nord à la Meunière'},
            'descriptions': {'en': 'Whole North Sea sole pan-fried in brown butter', 'nl': 'Hele Noordzeeton gebakken in bruine boter', 'fr': 'Sole entière de la Mer du Nord poêlée au beurre noir'},
        },
        # Desserts - Belgian Style
        {
            'category': 'desserts',
            'price': '7.50',
            'names': {'en': 'Waffle with Chocolate', 'nl': 'Wafel met Chocolade', 'fr': 'Gaufre au Chocolat'},
            'descriptions': {'en': 'Crispy Belgian waffle with dark chocolate and whipped cream', 'nl': 'Knapperige Belgische wafel met donkere chocolade en slagroom', 'fr': 'Gaufre belge croustillante avec chocolat noir et crème fouettée'},
        },
        {
            'category': 'desserts',
            'price': '8.00',
            'names': {'en': 'Liège Waffle', 'nl': 'Luikse Wafel', 'fr': 'Gaufre de Liège'},
            'descriptions': {'en': 'Traditional Liège waffle with pearl sugar and vanilla ice cream', 'nl': 'Traditionele Luikse wafel met parelsuiker en vanille-ijs', 'fr': 'Gaufre traditionnelle de Liège avec sucre perlé et glace vanille'},
        },
        {
            'category': 'desserts',
            'price': '6.50',
            'names': {'en': 'Belgian Chocolate Mousse', 'nl': 'Belgische Chocolademousse', 'fr': 'Mousse de Chocolat Belge'},
            'descriptions': {'en': 'Rich chocolate mousse made with Belgian Godiva chocolate', 'nl': 'Rijke chocolademousse gemaakt met Belgische Godiva-chocolade', 'fr': 'Mousse de chocolat riche faite avec du chocolat Godiva belge'},
        },
        {
            'category': 'desserts',
            'price': '7.00',
            'names': {'en': 'Praline Tart', 'nl': 'Praline Taart', 'fr': 'Tarte aux Pralines'},
            'descriptions': {'en': 'Belgian praline chocolate tart with hazelnut cream', 'nl': 'Belgische praline-chocoladetaart met hazelnootroom', 'fr': 'Tarte au chocolat praliné belge avec crème de noisette'},
        },
        {
            'category': 'desserts',
            'price': '6.00',
            'names': {'en': 'Panna Cotta', 'nl': 'Panna Cotta', 'fr': 'Panna Cotta'},
            'descriptions': {'en': 'Silky panna cotta with Belgian chocolate and berries', 'nl': 'Zijdezachte panna cotta met Belgische chocolade en bessen', 'fr': 'Panna cotta soyeuse avec chocolat belge et fruits rouges'},
        },
        # Beverages - Belgian Beers & Drinks
        {
            'category': 'beverages',
            'price': '3.50',
            'names': {'en': 'Fresh Orange Juice', 'nl': 'Vers Sinaasappelsap', 'fr': 'Jus d\'Orange Frais'},
            'descriptions': {'en': 'Freshly squeezed orange juice', 'nl': 'Vers geperst sinaasappelsap', 'fr': 'Jus d\'orange fraîchement pressé'},
        },
        {
            'category': 'beverages',
            'price': '2.50',
            'names': {'en': 'Belgian Beer - Trappist', 'nl': 'Belgisch Bier - Trappist', 'fr': 'Bière Belge - Trappiste'},
            'descriptions': {'en': 'Authentic Trappist beer from Belgian monastery', 'nl': 'Authentiek Trappistenbier van Belgische klooster', 'fr': 'Bière Trappiste authentique du monastère belge'},
        },
        {
            'category': 'beverages',
            'price': '2.00',
            'names': {'en': 'Lambic Beer', 'nl': 'Lambic Bier', 'fr': 'Bière Lambic'},
            'descriptions': {'en': 'Traditional Belgian sour wheat beer from Brussels', 'nl': 'Traditioneel Belgisch zuur witbier uit Brussel', 'fr': 'Bière de blé acide traditionnelle belge de Bruxelles'},
        },
        {
            'category': 'beverages',
            'price': '3.00',
            'names': {'en': 'Dubbel Beer', 'nl': 'Dubbel Bier', 'fr': 'Bière Dubbel'},
            'descriptions': {'en': 'Rich and malty Belgian Dubbel beer', 'nl': 'Rijke en moutachtige Belgische Dubbel bier', 'fr': 'Bière Dubbel belge riche et maltée'},
        },
        {
            'category': 'beverages',
            'price': '4.00',
            'names': {'en': 'Belgian Hot Chocolate', 'nl': 'Belgische Hete Chocolade', 'fr': 'Chocolat Chaud Belge'},
            'descriptions': {'en': 'Rich hot chocolate made with Belgian chocolate', 'nl': 'Rijke warme chocolade gemaakt van Belgische chocolade', 'fr': 'Chocolat chaud riche fait avec du chocolat belge'},
        },
        {
            'category': 'beverages',
            'price': '2.50',
            'names': {'en': 'Coffee - Espresso', 'nl': 'Koffie - Espresso', 'fr': 'Café - Espresso'},
            'descriptions': {'en': 'Strong Italian-style espresso', 'nl': 'Sterke Italiaans-stijl espresso', 'fr': 'Espresso forte style italien'},
        },
    ]
    
    for item_data in menu_items:
        item, created = MenuItem.objects.get_or_create(
            category=item_data['category'],
            price=item_data['price'],
            defaults={'order': 0}
        )
        
        # Set translations
        for lang_code, name in item_data['names'].items():
            activate(lang_code)
            item.set_current_language(lang_code)
            item.name = name
            item.description = item_data['descriptions'].get(lang_code, '')
            item.save()
        
        print(f"  - {item_data['names']['en']}: {'Created' if created else 'Already exists'}")
    
    print("\n" + "=" * 60)
    print("✓ Database setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python manage.py createsuperuser")
    print("2. Run: python manage.py runserver")
    print("3. Visit: http://localhost:8000/admin/")
    print("4. Log in with your superuser credentials")
    print("=" * 60)


if __name__ == '__main__':
    setup_database()
