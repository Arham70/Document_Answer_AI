from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Document
from .forms import DocumentUploadForm
from .utils import extract_text_from_pdf, process_document_embeddings
import os

@login_required
def document_list(request):
    """List all user documents"""
    documents = Document.objects.filter(user=request.user)
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_upload(request):
    """Upload new document"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.file_size = document.file.size
            
            # Save the document first so the file gets saved to disk
            document.save()
            
            # Extract text from PDF
            try:
                text = extract_text_from_pdf(document.file.path)
                document.word_count = len(text.split())
                document.save()  # Save again with word count
                
                # Process embeddings
                process_document_embeddings(document.id)
                
                messages.success(request, 'Document uploaded successfully! Processing...')
                return redirect('documents:document_list')
            except Exception as e:
                messages.error(request, f'Error processing document: {str(e)}')
                # Don't redirect on error, show the form again with error
                return render(request, 'documents/document_upload.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DocumentUploadForm()
    
    return render(request, 'documents/document_upload.html', {'form': form})

@login_required
def document_detail(request, document_id):
    """Document detail view"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    return render(request, 'documents/document_detail.html', {'document': document})

@login_required
def document_delete(request, document_id):
    """Delete document"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully!')
        return redirect('documents:document_list')
    return render(request, 'documents/document_confirm_delete.html', {'document': document})