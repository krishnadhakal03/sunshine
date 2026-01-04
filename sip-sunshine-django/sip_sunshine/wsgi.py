"""
WSGI config for sip_sunshine project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip_sunshine.settings.development')

application = get_wsgi_application()
