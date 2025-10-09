#!/bin/bash

# DocuMind Deployment Script
echo "🚀 Starting DocuMind deployment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@documind.ai', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

echo "✅ Deployment completed successfully!"
echo "🌐 Your DocuMind application is ready!"
echo "📝 Admin credentials: admin / admin123"
echo "🔗 Access your application at: http://localhost:8000"
