from django.contrib import admin
from django.contrib.admin import AdminSite

class SipAndSunshineAdminSite(AdminSite):
    """Custom Admin Site for Sip and Sunshine Restaurant"""
    
    site_header = "Sip and SunShine Restaurant"
    site_title = "Sip and SunShine Admin"
    index_title = "Welcome to Admin Portal"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize admin UI
        self.disable_action('delete_selected')  # Make delete action safer


# Create custom admin site instance
admin_site = SipAndSunshineAdminSite(name='restaurant_admin')
