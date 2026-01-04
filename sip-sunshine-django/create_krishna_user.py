#!/usr/bin/env python
"""Create Krishna admin user"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip_sunshine.settings.development')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

print("=" * 60)
print("CREATING ADMIN USER")
print("=" * 60)

try:
    # Check database connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✓ Database connection successful\n")
    
    # Delete existing krishna user if exists
    User.objects.filter(username='krishna').delete()
    print("✓ Cleared any existing 'krishna' user")
    
    # Create new superuser
    user = User.objects.create_superuser('krishna', 'krishna@restaurant.local', 'admin123')
    
    print("\n" + "=" * 60)
    print("✓ ADMIN USER CREATED SUCCESSFULLY!")
    print("=" * 60)
    print("\nLogin Credentials:")
    print("-" * 60)
    print(f"  Username: krishna")
    print(f"  Password: admin123")
    print(f"  Email:    krishna@restaurant.local")
    print(f"  URL:      http://localhost:2005/admin/")
    print("-" * 60)
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
