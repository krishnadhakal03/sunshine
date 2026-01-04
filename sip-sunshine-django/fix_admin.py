#!/usr/bin/env python
"""Fix admin user setup"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip_sunshine.settings.development')

# Setup Django without running app ready methods that might fail
import django.conf

if not django.conf.settings.configured:
    django.setup()

# Now import what we need
from django.contrib.auth.models import User
from django.db import connection

print("=" * 60)
print("ADMIN USER SETUP")
print("=" * 60)

try:
    # Check if database is accessible
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✓ Database connection successful")
    
    # Get or create admin user
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@restaurant.local',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )
    
    # Always update password
    user.set_password('admin123456')
    user.save()
    
    if created:
        print("✓ Admin user CREATED")
    else:
        print("✓ Admin user FOUND - password updated")
    
    print("\nLogin Credentials:")
    print("-" * 60)
    print(f"  Username: admin")
    print(f"  Password: admin123456")
    print(f"  URL:      http://localhost:2005/admin/")
    print("-" * 60)
    print("\n✓ Setup complete!")
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
