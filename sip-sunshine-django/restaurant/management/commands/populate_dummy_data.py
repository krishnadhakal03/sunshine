import os
import django
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from restaurant.models import Language, SiteSetting, Page, MenuItem, BlogPost, Reservation, ContentBlock
from django.utils import timezone
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with dummy data matching Kusina template'

    def handle(self, *args, **options):
        self.stdout.write('Starting dummy data creation...\n')
        
        # Create languages
        self.create_languages()
        
        # Create site settings
        self.create_site_settings()
        
        # Create pages
        self.create_pages()
        
        # Create menu items
        self.create_menu_items()
        
        # Create blog posts
        self.create_blog_posts()
        
        self.stdout.write(self.style.SUCCESS('\nDummy data created successfully!'))

    def create_languages(self):
        """Create supported languages"""
        self.stdout.write('Creating languages...')
        
        languages_data = [
            {'code': 'en', 'name': 'English', 'is_default': True},
            {'code': 'nl', 'name': 'Dutch', 'is_default': False},
            {'code': 'fr', 'name': 'French', 'is_default': False},
        ]
        
        for lang_data in languages_data:
            lang, created = Language.objects.get_or_create(
                code=lang_data['code'],
                defaults={
                    'name': lang_data['name'],
                    'is_active': True,
                    'is_default': lang_data['is_default'],
                }
            )
            if created:
                self.stdout.write(f"  Created language: {lang.name}")

    def create_site_settings(self):
        """Create site settings"""
        self.stdout.write('Creating site settings...')
        
        settings, created = SiteSetting.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Sip and SunShine - Restaurant',
                'site_description': 'Premium restaurant offering fine dining experience with authentic cuisine and warm hospitality.',
                'site_keywords': 'restaurant, fine dining, food, cuisine, reservation',
                'email': 'info@sipandsunshine.com',
                'phone': '+1 (555) 123-4567',
                'address': '123 Culinary Street, Food City, FC 12345',
                'facebook_url': 'https://facebook.com/sipandsunshine',
                'instagram_url': 'https://instagram.com/sipandsunshine',
                'twitter_url': 'https://twitter.com/sipandsunshine',
                'google_map_embed': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3024.1234567890!2d-74.0123456!3d40.7123456!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zNDDCsDQyJzQ0LjciTiA3NMKwMDAnNDguNyJX!5e0!3m2!1sen!2sus!4v1234567890" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
            }
        )
        
        if created:
            self.stdout.write('  Created site settings')

    def create_pages(self):
        """Create website pages with multi-language content"""
        self.stdout.write('Creating pages...')
        
        pages_data = [
            {
                'slug': 'home',
                'template_name': 'index',
                'is_homepage': True,
                'order': 1,
                'translations': {
                    'en': {
                        'title': 'Home',
                        'meta_title': 'Sip and SunShine - Premium Restaurant',
                        'meta_description': 'Experience fine dining at its best. Reserve your table today.',
                        'meta_keywords': 'restaurant, dining, reservations',
                        'content': '<h2>Eat Healthy and Natural Foods</h2><p>A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.</p>',
                    },
                    'nl': {
                        'title': 'Thuis',
                        'meta_title': 'Sip and SunShine - Premium Restaurant',
                        'meta_description': 'Ervaar heerlijk dineren op zijn best.',
                        'meta_keywords': 'restaurant, eten, reserveringen',
                        'content': '<h2>Eet Gezond en Natuurlijk Voedsel</h2><p>Een kleine rivier genaamd Duden stroomt voorbij hun plaats en voorziet het van de nodige regelialia.</p>',
                    },
                    'fr': {
                        'title': 'Accueil',
                        'meta_title': 'Sip and SunShine - Restaurant Premium',
                        'meta_description': 'Découvrez une fine cuisine dans le meilleur style.',
                        'meta_keywords': 'restaurant, cuisine, réservations',
                        'content': '<h2>Mangez sainement et naturel</h2><p>Un petit fleuve nommé Duden coule près de leur place et la ravitaille en reglealia nécessaire.</p>',
                    }
                }
            },
            {
                'slug': 'about',
                'template_name': 'about',
                'is_homepage': False,
                'order': 2,
                'translations': {
                    'en': {
                        'title': 'About Us',
                        'meta_title': 'About Sip and SunShine',
                        'meta_description': 'Learn about our restaurant and our mission.',
                        'meta_keywords': 'about, restaurant, history',
                        'content': '<h2>About Our Restaurant</h2><p>Founded in 2010, Sip and SunShine has been serving exquisite dishes to our valued guests for over a decade. Our commitment to quality ingredients and exceptional service sets us apart.</p><p>Our team of expert chefs brings culinary artistry to every plate, creating unforgettable dining experiences. We source the finest ingredients from local and international suppliers to ensure the highest quality.</p>',
                    },
                    'nl': {
                        'title': 'Over Ons',
                        'meta_title': 'Over Sip and SunShine',
                        'meta_description': 'Leer over ons restaurant en onze missie.',
                        'meta_keywords': 'over, restaurant, geschiedenis',
                        'content': '<h2>Over ons restaurant</h2><p>Opgericht in 2010, serveert Sip and SunShine meer dan een decennium lang heerlijke gerechten aan onze gewaardeerde gasten.</p>',
                    },
                    'fr': {
                        'title': 'À Propos',
                        'meta_title': 'À Propos de Sip and SunShine',
                        'meta_description': 'En savoir plus sur notre restaurant et notre mission.',
                        'meta_keywords': 'à propos, restaurant, histoire',
                        'content': '<h2>À Propos de Notre Restaurant</h2><p>Fondé en 2010, Sip and SunShine sert des plats exquis à nos clients estimés depuis plus d\'une décennie.</p>',
                    }
                }
            },
            {
                'slug': 'menu',
                'template_name': 'menu',
                'is_homepage': False,
                'order': 3,
                'translations': {
                    'en': {
                        'title': 'Our Menu - Specialties',
                        'meta_title': 'Menu | Sip and SunShine',
                        'meta_description': 'Explore our delicious menu offerings.',
                        'meta_keywords': 'menu, food, specialties',
                        'content': '<h2>Specialties</h2><p>Our menu features a selection of carefully crafted dishes prepared by our experienced chefs using only the finest ingredients.</p>',
                    },
                    'nl': {
                        'title': 'Ons Menu - Specialiteiten',
                        'meta_title': 'Menu | Sip and SunShine',
                        'meta_description': 'Ontdek ons heerlijke menu.',
                        'meta_keywords': 'menu, voedsel, specialiteiten',
                        'content': '<h2>Specialiteiten</h2><p>Ons menu biedt een selectie van zorgvuldig bereide gerechten door onze ervaren chef-koks.</p>',
                    },
                    'fr': {
                        'title': 'Notre Menu - Spécialités',
                        'meta_title': 'Menu | Sip and SunShine',
                        'meta_description': 'Découvrez nos délicieux plats.',
                        'meta_keywords': 'menu, nourriture, spécialités',
                        'content': '<h2>Spécialités</h2><p>Notre menu propose une sélection de plats soigneusement préparés par nos chefs expérimentés.</p>',
                    }
                }
            },
            {
                'slug': 'blog',
                'template_name': 'blog',
                'is_homepage': False,
                'order': 4,
                'translations': {
                    'en': {
                        'title': 'Stories & Blog',
                        'meta_title': 'Blog | Sip and SunShine',
                        'meta_description': 'Read our latest stories and culinary insights.',
                        'meta_keywords': 'blog, stories, food, recipes',
                        'content': '<h2>Latest Stories</h2><p>Discover culinary insights, chef tips, and restaurant news from Sip and SunShine.</p>',
                    },
                    'nl': {
                        'title': 'Verhalen & Blog',
                        'meta_title': 'Blog | Sip and SunShine',
                        'meta_description': 'Lees ons laatste verhalen.',
                        'meta_keywords': 'blog, verhalen, voedsel, recepten',
                        'content': '<h2>Laatste Verhalen</h2><p>Ontdek culinaire inzichten van Sip and SunShine.</p>',
                    },
                    'fr': {
                        'title': 'Histoires & Blog',
                        'meta_title': 'Blog | Sip and SunShine',
                        'meta_description': 'Lisez nos dernières histoires.',
                        'meta_keywords': 'blog, histoires, nourriture, recettes',
                        'content': '<h2>Dernières Histoires</h2><p>Découvrez les perspectives culinaires de Sip and SunShine.</p>',
                    }
                }
            },
            {
                'slug': 'contact',
                'template_name': 'contact',
                'is_homepage': False,
                'order': 5,
                'translations': {
                    'en': {
                        'title': 'Contact Us',
                        'meta_title': 'Contact | Sip and SunShine',
                        'meta_description': 'Get in touch with us for reservations and inquiries.',
                        'meta_keywords': 'contact, reservations, inquiry',
                        'content': '<h2>Contact Information</h2><p>Have questions? We\'d love to hear from you. Contact us using the form below or reach out directly.</p>',
                    },
                    'nl': {
                        'title': 'Neem Contact Op',
                        'meta_title': 'Contact | Sip and SunShine',
                        'meta_description': 'Neem contact met ons op.',
                        'meta_keywords': 'contact, reserveringen, onderzoek',
                        'content': '<h2>Contactgegevens</h2><p>Heb je vragen? Wij horen graag van je.</p>',
                    },
                    'fr': {
                        'title': 'Nous Contacter',
                        'meta_title': 'Contact | Sip and SunShine',
                        'meta_description': 'Prenez contact avec nous.',
                        'meta_keywords': 'contact, réservations, demande',
                        'content': '<h2>Informations de Contact</h2><p>Avez-vous des questions ? Nous aimerions avoir de vos nouvelles.</p>',
                    }
                }
            },
            {
                'slug': 'reservation',
                'template_name': 'reservation',
                'is_homepage': False,
                'order': 6,
                'translations': {
                    'en': {
                        'title': 'Make a Reservation',
                        'meta_title': 'Reservation | Sip and SunShine',
                        'meta_description': 'Book your table at our restaurant.',
                        'meta_keywords': 'reservation, booking, table',
                        'content': '<h2>Book Your Table</h2><p>Reserve your table at Sip and SunShine and enjoy an unforgettable dining experience.</p>',
                    },
                    'nl': {
                        'title': 'Een Reservering Maken',
                        'meta_title': 'Reservering | Sip and SunShine',
                        'meta_description': 'Reserveer uw tafel in ons restaurant.',
                        'meta_keywords': 'reservering, boeking, tafel',
                        'content': '<h2>Uw Tafel Reserveren</h2><p>Reserveer uw tafel in Sip and SunShine.</p>',
                    },
                    'fr': {
                        'title': 'Faire une Réservation',
                        'meta_title': 'Réservation | Sip and SunShine',
                        'meta_description': 'Réservez votre table dans notre restaurant.',
                        'meta_keywords': 'réservation, réservation, table',
                        'content': '<h2>Réservez Votre Table</h2><p>Réservez votre table chez Sip and SunShine.</p>',
                    }
                }
            },
        ]
        
        for page_data in pages_data:
            translations = page_data.pop('translations')
            page, created = Page.objects.get_or_create(
                slug=page_data['slug'],
                defaults=page_data
            )
            
            # Add translations for each language
            for lang_code, trans_data in translations.items():
                page.translations.update_or_create(language_code=lang_code, defaults=trans_data)
            
            if created:
                self.stdout.write(f"  Created page: {page.slug}")
            else:
                self.stdout.write(f"  Updated page: {page.slug}")

    def create_menu_items(self):
        """Create menu items with translations"""
        self.stdout.write('Creating menu items...')
        
        menu_data = [
            # Appetizers
            {
                'category': 'appetizers',
                'price': Decimal('12.99'),
                'translations': {
                    'en': {'name': 'Fresh Oysters', 'description': 'Served with lemon and cocktail sauce'},
                    'nl': {'name': 'Verse Oesters', 'description': 'Geserveerd met citroen en cocktailsaus'},
                    'fr': {'name': 'Huîtres Fraîches', 'description': 'Servies avec citron et sauce cocktail'},
                }
            },
            {
                'category': 'appetizers',
                'price': Decimal('14.99'),
                'translations': {
                    'en': {'name': 'Shrimp Tempura', 'description': 'Crispy battered shrimp with dipping sauce'},
                    'nl': {'name': 'Garnalen Tempura', 'description': 'Krokante gefrituurde garnalen'},
                    'fr': {'name': 'Crevettes Tempura', 'description': 'Crevettes croustillantes en pâte'},
                }
            },
            {
                'category': 'appetizers',
                'price': Decimal('13.99'),
                'translations': {
                    'en': {'name': 'Foie Gras Mousse', 'description': 'Smooth liver mousse with toast points'},
                    'nl': {'name': 'Foie Gras Mousse', 'description': 'Gladde levertaart met toast'},
                    'fr': {'name': 'Mousse de Foie Gras', 'description': 'Mousse de foie lisse avec pain grillé'},
                }
            },
            
            # Main Courses
            {
                'category': 'main_courses',
                'price': Decimal('34.99'),
                'translations': {
                    'en': {'name': 'Australian Organic Beef', 'description': 'Grilled to perfection with seasonal vegetables'},
                    'nl': {'name': 'Australisch Bio Rundvlees', 'description': 'Gegrild naar perfectie met seizoensgroenten'},
                    'fr': {'name': 'Boeuf Biologique Australien', 'description': 'Grillé à la perfection avec légumes de saison'},
                }
            },
            {
                'category': 'main_courses',
                'price': Decimal('42.99'),
                'translations': {
                    'en': {'name': 'Atlantic Lobster Tail', 'description': 'Butter-poached lobster with garlic sauce'},
                    'nl': {'name': 'Atlantische Zoetwaterkreeft', 'description': 'Zoetwaterkreeft in botersaus'},
                    'fr': {'name': 'Queue de Homard Atlantique', 'description': 'Homard poché au beurre avec sauce à l\'ail'},
                }
            },
            {
                'category': 'main_courses',
                'price': Decimal('38.99'),
                'translations': {
                    'en': {'name': 'Chilean Sea Bass', 'description': 'Pan-seared with lemon butter and capers'},
                    'nl': {'name': 'Chileense Zeebaars', 'description': 'Gebakken in botersaus met kappertjes'},
                    'fr': {'name': 'Bar Chilien', 'description': 'Poêlé avec beurre citron et câpres'},
                }
            },
            {
                'category': 'main_courses',
                'price': Decimal('36.99'),
                'translations': {
                    'en': {'name': 'Duck Confit', 'description': 'Slow-roasted duck leg with cherry gastrique'},
                    'nl': {'name': 'Eendenconfit', 'description': 'Langzaam geroosterde eendenbout'},
                    'fr': {'name': 'Confit de Canard', 'description': 'Cuisse de canard rôtie lentement'},
                }
            },
            
            # Desserts
            {
                'category': 'desserts',
                'price': Decimal('9.99'),
                'translations': {
                    'en': {'name': 'Chocolate Lava Cake', 'description': 'Warm chocolate cake with vanilla ice cream'},
                    'nl': {'name': 'Chocolade Lava Taart', 'description': 'Warme chocoladetaart met vanille-ijs'},
                    'fr': {'name': 'Gâteau Fondant au Chocolat', 'description': 'Gâteau chaud avec crème glacée à la vanille'},
                }
            },
            {
                'category': 'desserts',
                'price': Decimal('11.99'),
                'translations': {
                    'en': {'name': 'Crème Brûlée', 'description': 'Classic French custard with caramelized sugar'},
                    'nl': {'name': 'Crème Brûlée', 'description': 'Klassieke Franse custard met karamelsuiker'},
                    'fr': {'name': 'Crème Brûlée', 'description': 'Crème pâtissière française classique'},
                }
            },
            {
                'category': 'desserts',
                'price': Decimal('8.99'),
                'translations': {
                    'en': {'name': 'Tiramisu', 'description': 'Italian dessert with mascarpone and coffee'},
                    'nl': {'name': 'Tiramisu', 'description': 'Italiaans dessert met mascarpone en koffie'},
                    'fr': {'name': 'Tiramisu', 'description': 'Dessert italien avec mascarpone et café'},
                }
            },
            
            # Beverages
            {
                'category': 'beverages',
                'price': Decimal('6.99'),
                'translations': {
                    'en': {'name': 'House Wine', 'description': 'Premium selection of red or white wine'},
                    'nl': {'name': 'Huiswijn', 'description': 'Premium selectie rode of witte wijn'},
                    'fr': {'name': 'Vin Maison', 'description': 'Sélection premium de vin rouge ou blanc'},
                }
            },
            {
                'category': 'beverages',
                'price': Decimal('5.99'),
                'translations': {
                    'en': {'name': 'Craft Beer', 'description': 'Local craft beer selection'},
                    'nl': {'name': 'Ambachtsbier', 'description': 'Lokale ambachtsbier selectie'},
                    'fr': {'name': 'Bière Artisanale', 'description': 'Sélection de bière artisanale locale'},
                }
            },
            
            # Drinks
            {
                'category': 'drinks',
                'price': Decimal('8.99'),
                'translations': {
                    'en': {'name': 'Fresh Mojito', 'description': 'Mint, lime, rum, and soda'},
                    'nl': {'name': 'Verse Mojito', 'description': 'Munt, limoen, rum en soda'},
                    'fr': {'name': 'Mojito Frais', 'description': 'Menthe, citron vert, rhum et soda'},
                }
            },
            {
                'category': 'drinks',
                'price': Decimal('9.99'),
                'translations': {
                    'en': {'name': 'House Cocktail', 'description': 'Our signature mixed drink'},
                    'nl': {'name': 'Huiscocktail', 'description': 'Onze signature gemengde drank'},
                    'fr': {'name': 'Cocktail Signature', 'description': 'Notre cocktail signature'},
                }
            },
        ]
        
        for item_data in menu_data:
            translations = item_data.pop('translations')
            item = MenuItem.objects.create(
                category=item_data['category'],
                price=item_data['price'],
            )
            
            # Add translations
            for lang_code, trans_data in translations.items():
                item.translations.update_or_create(language_code=lang_code, defaults=trans_data)
            
            self.stdout.write(f"  Created menu item: {item_data['category']}")

    def create_blog_posts(self):
        """Create blog posts with translations"""
        self.stdout.write('Creating blog posts...')
        
        blog_data = [
            {
                'slug': 'healthy-eating-tips',
                'translations': {
                    'en': {
                        'title': 'Healthy Eating Tips for Busy Professionals',
                        'excerpt': 'Discover how to maintain a healthy diet while managing a busy schedule.',
                        'content': '<h2>Healthy Eating Tips</h2><p>Eating healthy doesn\'t have to be complicated. Here are some simple tips to help you maintain a balanced diet even when you\'re busy.</p><p>1. Plan your meals in advance</p><p>2. Keep healthy snacks available</p><p>3. Stay hydrated</p><p>4. Choose whole grains</p><p>5. Incorporate more vegetables</p>',
                    },
                    'nl': {
                        'title': 'Gezonde Eettips voor Drukke Professionals',
                        'excerpt': 'Ontdek hoe je gezond eet ondanks een druk schema.',
                        'content': '<h2>Gezonde Eettips</h2><p>Gezond eten hoeft niet ingewikkeld te zijn. Hier zijn enkele eenvoudige tips.</p>',
                    },
                    'fr': {
                        'title': 'Conseils Alimentaires Sains pour les Professionnels Occupés',
                        'excerpt': 'Découvrez comment maintenir une alimentation saine.',
                        'content': '<h2>Conseils Alimentaires Sains</h2><p>Manger sainement ne doit pas être compliqué.</p>',
                    }
                }
            },
            {
                'slug': 'culinary-traditions',
                'translations': {
                    'en': {
                        'title': 'Exploring Culinary Traditions Around the World',
                        'excerpt': 'Journey through different cultures and their unique food traditions.',
                        'content': '<h2>World Culinary Traditions</h2><p>Every culture has unique food traditions that reflect its history and values. Explore the diverse culinary landscapes of the world.</p><p>Asian Cuisine: Rich in flavors and spices</p><p>European Cuisine: Classic techniques and refined tastes</p><p>African Cuisine: Bold flavors and authentic recipes</p><p>Latin American Cuisine: Vibrant and colorful dishes</p>',
                    },
                    'nl': {
                        'title': 'Culinaire Tradities Wereldwijd Verkennen',
                        'excerpt': 'Ontdek verschillende culturen en hun unieke voedseltradities.',
                        'content': '<h2>Wereldwijde Culinaire Tradities</h2><p>Elke cultuur heeft unieke voedseltradities.</p>',
                    },
                    'fr': {
                        'title': 'Explorer les Traditions Culinaires du Monde',
                        'excerpt': 'Découvrez différentes cultures et leurs traditions culinaires uniques.',
                        'content': '<h2>Traditions Culinaires Mondiales</h2><p>Chaque culture a des traditions culinaires uniques.</p>',
                    }
                }
            },
            {
                'slug': 'wine-pairing-guide',
                'translations': {
                    'en': {
                        'title': 'Complete Wine Pairing Guide for Every Dish',
                        'excerpt': 'Learn how to pair wines with different dishes to enhance your dining experience.',
                        'content': '<h2>Wine Pairing Guide</h2><p>Proper wine pairing can elevate your dining experience. Here\'s how to match wines with different dishes.</p><p>Red Wine: Pairs well with red meat and hearty dishes</p><p>White Wine: Perfect with seafood and light meals</p><p>Rosé: Versatile and works with many cuisines</p><p>Sparkling: Great for appetizers and celebrations</p>',
                    },
                    'nl': {
                        'title': 'Compleet Wijnpaarings Gids',
                        'excerpt': 'Leer hoe je wijnen combineert met verschillende gerechten.',
                        'content': '<h2>Wijnpaarings Gids</h2><p>Juiste wijnafstemming kan uw dinerervaring verbeteren.</p>',
                    },
                    'fr': {
                        'title': 'Guide Complet d\'Accords Mets-Vins',
                        'excerpt': 'Apprenez à associer les vins avec différents plats.',
                        'content': '<h2>Guide d\'Accords Mets-Vins</h2><p>Les accords mets-vins appropriés peuvent améliorer votre expérience culinaire.</p>',
                    }
                }
            },
            {
                'slug': 'chef-interview',
                'translations': {
                    'en': {
                        'title': 'Interview with Our Head Chef: Behind the Kitchen Scenes',
                        'excerpt': 'Meet our talented chef and learn about their culinary journey and philosophy.',
                        'content': '<h2>Chef Interview</h2><p>Our head chef brings passion and creativity to every dish. Learn about their culinary philosophy and journey in the kitchen.</p><p>Q: What inspired you to become a chef?</p><p>A: I\'ve always been passionate about bringing joy to people through food.</p>',
                    },
                    'nl': {
                        'title': 'Interview met Onze Chef-kok',
                        'excerpt': 'Ontmoet onze talentvolle chef-kok.',
                        'content': '<h2>Chef-kok Interview</h2><p>Onze chef-kok brengt passie en creativiteit in elk gerecht.</p>',
                    },
                    'fr': {
                        'title': 'Entretien Avec Notre Chef de Cuisine',
                        'excerpt': 'Rencontrez notre chef talentueux.',
                        'content': '<h2>Entretien Avec le Chef</h2><p>Notre chef apporte passion et créativité à chaque plat.</p>',
                    }
                }
            },
            {
                'slug': 'seasonal-menu-update',
                'translations': {
                    'en': {
                        'title': 'Our New Seasonal Menu is Here!',
                        'excerpt': 'Discover fresh seasonal dishes featuring local ingredients.',
                        'content': '<h2>Seasonal Menu Update</h2><p>This season, we\'re excited to introduce new dishes featuring the freshest seasonal ingredients from local farmers.</p><p>Spring: Fresh vegetables and light preparations</p><p>Summer: Grilled specialties and refreshing drinks</p><p>Fall: Rich flavors and comfort food</p><p>Winter: Hearty dishes and warming beverages</p>',
                    },
                    'nl': {
                        'title': 'Ons Nieuwe Seizoensgebonden Menu is Hier!',
                        'excerpt': 'Ontdek verse seizoensgebonden gerechten.',
                        'content': '<h2>Seizoensgebonden Menuupdate</h2><p>Dit seizoen presenteren we nieuwe gerechten met vers seizoensgebonden ingrediënten.</p>',
                    },
                    'fr': {
                        'title': 'Notre Nouveau Menu Saisonnier est Arrivé!',
                        'excerpt': 'Découvrez de nouveaux plats saisonniers.',
                        'content': '<h2>Mise à Jour du Menu Saisonnier</h2><p>Cette saison, nous présentons de nouveaux plats avec les ingrédients saisonniers les plus frais.</p>',
                    }
                }
            },
        ]
        
        for blog_data in blog_data:
            translations = blog_data.pop('translations')
            blog = BlogPost.objects.create(
                slug=blog_data['slug'],
                author='Sip and SunShine Team',
                is_published=True,
                published_at=timezone.now(),
            )
            
            # Add translations
            for lang_code, trans_data in translations.items():
                blog.translations.update_or_create(language_code=lang_code, defaults=trans_data)
            
            self.stdout.write(f"  Created blog post: {blog_data['slug']}")
