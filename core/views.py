from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from documents.models import Document
from chat.models import ChatSession

def is_openai_configured():
    """Check if OpenAI API key is properly configured"""
    if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
        return False
    
    # Check if it's a placeholder or invalid key
    key = settings.OPENAI_API_KEY.strip()
    if (key == 'your-openai-api-key-here' or 
        key == 'key_here' or 
        not key.startswith('sk-') or 
        len(key) < 20):
        return False
    
    return True

def home(request):
    """Landing page with attractive design and information"""
    context = {
        'total_users': User.objects.count(),
        'total_documents': Document.objects.count(),
        'total_chats': ChatSession.objects.count(),
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page"""
    return render(request, 'core/about.html')

@login_required
def dashboard(request):
    """User dashboard"""
    user_documents = Document.objects.filter(user=request.user)
    recent_chats = ChatSession.objects.filter(user=request.user)[:5]
    
    context = {
        'documents': user_documents,
        'recent_chats': recent_chats,
        'total_documents': user_documents.count(),
        'total_chats': ChatSession.objects.filter(user=request.user).count(),
        'openai_configured': is_openai_configured(),
    }
    return render(request, 'core/dashboard.html', context)