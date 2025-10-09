@echo off
REM DocuMind Deployment Script for Windows
echo 🚀 Starting DocuMind deployment...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🐍 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo 🗄️ Running database migrations...
python manage.py migrate

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

REM Create superuser if it doesn't exist
echo 👤 Creating superuser...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@documind.ai', 'admin123') if not User.objects.filter(username='admin').exists() else print('Superuser already exists')"

echo ✅ Deployment completed successfully!
echo 🌐 Your DocuMind application is ready!
echo 📝 Admin credentials: admin / admin123
echo 🔗 Access your application at: http://localhost:8000
pause
