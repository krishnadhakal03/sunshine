from django.apps import AppConfig


class RestaurantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'
    verbose_name = 'Restaurant Management'
    
    def ready(self):
        # Initialize default languages and site settings when the app is ready
        from .models import Language, SiteSetting
        
        try:
            # Create default languages if they don't exist
            languages = [
                {'code': 'en', 'name': 'English', 'is_default': True},
                {'code': 'nl', 'name': 'Dutch (Nederlands)', 'is_default': False},
                {'code': 'fr', 'name': 'French (Français)', 'is_default': False},
            ]
            
            for lang in languages:
                Language.objects.get_or_create(
                    code=lang['code'],
                    defaults={'name': lang['name'], 'is_default': lang['is_default']}
                )
            
            # Create default site settings if they don't exist
            if not SiteSetting.objects.exists():
                SiteSetting.objects.create(
                    site_name='Sip and SunShine',
                    email='info@sipandsunshine.com',
                    phone='+31 (0)6 12345678',
                    address='123 Restaurant Street, Amsterdam, Netherlands'
                )
        except Exception:
            # Database may not be ready yet, that's fine
            pass
