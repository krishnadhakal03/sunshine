#!/usr/bin/env python
"""
Quick fix: Ensure pages exist and display properly
Run this if pages appear blank or empty
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip_sunshine.settings.development')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from restaurant.models import Page
from django.utils.translation import activate

print("\n" + "=" * 60)
print("FIXING BLANK PAGES - Creating Page Records")
print("=" * 60)

# Ensure all required pages exist
pages_to_create = [
    ('contact', 'contact'),
    ('reservation', 'reservation'),
]

for slug, template in pages_to_create:
    page, created = Page.objects.get_or_create(
        slug=slug,
        defaults={
            'template_name': template,
            'is_active': True,
            'order': 5 if slug == 'contact' else 6,
            'title': slug.replace('_', ' ').title(),
        }
    )
    
    if created:
        print(f"✅ Created: {slug}")
    else:
        # Make sure it's active
        if not page.is_active:
            page.is_active = True
            page.save()
            print(f"🔄 Reactivated: {slug}")
        else:
            print(f"✓ Already exists: {slug}")

print("\n" + "=" * 60)
print("DONE! Pages should now display properly")
print("=" * 60)
print("\nIf pages still blank:")
print("1. Run: python setup_db.py")
print("2. Verify in admin: http://localhost:2005/admin/")
print("3. Check Page records are active")
