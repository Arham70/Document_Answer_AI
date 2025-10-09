from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
import json
from .models import ChatSession, Message
from documents.models import Document
from documents.rag_utils import get_ai_response

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

@login_required
def chat_list(request):
    """List all chat sessions"""
    chat_sessions = ChatSession.objects.filter(user=request.user)
    return render(request, 'chat/chat_list.html', {'chat_sessions': chat_sessions})

@login_required
def chat_detail(request, chat_id):
    """Chat detail view"""
    chat_session = get_object_or_404(ChatSession, id=chat_id, user=request.user)
    messages = chat_session.messages.all()
    return render(request, 'chat/chat_detail.html', {
        'chat_session': chat_session,
        'messages': messages,
        'openai_configured': is_openai_configured()
    })

@login_required
def start_chat(request, document_id):
    """Start new chat session with document"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    
    if document.status != 'processed':
        messages.error(request, 'Document is not processed yet. Please wait.')
        return redirect('documents:document_detail', document_id=document_id)
    
    # Create new chat session
    chat_session = ChatSession.objects.create(
        user=request.user,
        document=document,
        title=f"Chat about {document.title}"
    )
    
    return redirect('chat:chat_detail', chat_id=chat_session.id)

@login_required
@require_POST
@csrf_exempt
def send_message(request, chat_id):
    """Send message and get AI response"""
    try:
        chat_session = get_object_or_404(ChatSession, id=chat_id, user=request.user)
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Save user message
        user_msg = Message.objects.create(
            chat_session=chat_session,
            role='user',
            content=user_message
        )
        
        # Get AI response
        try:
            if is_openai_configured():
                ai_response = get_ai_response(user_message, chat_session.document.embedding_id)
            else:
                ai_response = ("🔑 **OpenAI API Key Not Configured**\n\n"
                              "To use the AI chat functionality, please configure your OpenAI API key in the environment variables.\n\n"
                              "**Steps to configure:**\n"
                              "1. Get your API key from https://platform.openai.com/api-keys\n"
                              "2. Update the OPENAI_API_KEY in your .env file\n"
                              "3. Restart the application\n\n"
                              "**Current Status:** Document uploaded successfully, but AI chat is disabled.")
        except Exception as e:
            ai_response = f"Sorry, I encountered an error: {str(e)}"
        
        # Save AI message
        ai_msg = Message.objects.create(
            chat_session=chat_session,
            role='ai',
            content=ai_response
        )
        
        # Update chat session timestamp
        chat_session.updated_at = timezone.now()
        chat_session.save()
        
        return JsonResponse({
            'user_message': {
                'id': str(user_msg.id),
                'content': user_msg.content,
                'timestamp': user_msg.timestamp.isoformat()
            },
            'ai_message': {
                'id': str(ai_msg.id),
                'content': ai_msg.content,
                'timestamp': ai_msg.timestamp.isoformat()
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def export_chat(request, chat_id):
    """Export chat to DOCX"""
    from .utils import export_chat_to_docx
    
    chat_session = get_object_or_404(ChatSession, id=chat_id, user=request.user)
    
    try:
        file_path = export_chat_to_docx(chat_session)
        return JsonResponse({'download_url': file_path})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)