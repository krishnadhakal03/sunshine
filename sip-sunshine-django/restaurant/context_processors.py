from restaurant.models import SiteSetting, Language
from django.utils.translation import get_language


def site_settings(request):
    """Make site settings available to all templates"""
    try:
        settings = SiteSetting.objects.first()
    except:
        settings = None
    
    return {'site_settings': settings}


def active_languages(request):
    """Make active languages available to all templates"""
    try:
        languages = Language.objects.filter(is_active=True).order_by('-is_default')
    except:
        languages = []
    
    current_language = get_language()
    
    return {
        'active_languages': languages,
        'current_language': current_language,
    }
