#!/usr/bin/env python
"""
Quick script to populate database with dummy data
Run this after: python manage.py migrate
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip_sunshine.settings.development')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

# Now run setup
from setup_db import setup_database

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("POPULATING DATABASE WITH DUMMY DATA")
    print("=" * 60)
    
    try:
        setup_database()
        print("\n" + "=" * 60)
        print("SUCCESS! Dummy data has been added to database")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Visit: http://localhost:2005/admin/")
        print("2. Login: admin / admin123456")
        print("3. See Site Settings populated with dummy data")
        print("4. Go to: http://localhost:2005/contact/")
        print("5. Go to: http://localhost:2005/reservation/")
        print("\nThe pages should now display with dummy contact info!")
        print("\nReplace with real data from your customer when ready.")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
