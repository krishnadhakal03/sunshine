#!/bin/bash
# Quick Start Script for Sip and SunShine Django Project

echo "=========================================="
echo "Sip and SunShine - Django Setup Script"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate

# Initialize database
echo ""
echo "Initializing database with sample data..."
python setup_db.py

# Create superuser if needed
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create superuser: python manage.py createsuperuser"
echo "2. Run dev server: python manage.py runserver"
echo "3. Visit: http://localhost:8000/admin"
echo ""
echo "To run the server:"
echo "  python manage.py runserver"
echo ""
