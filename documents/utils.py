import fitz  # PyMuPDF
import os
from django.conf import settings
from django.utils import timezone
from .models import Document
from .rag_utils import create_embeddings, store_embeddings

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise Exception(f"PDF file not found at path: {file_path}")
        
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        if not text.strip():
            raise Exception("No text content found in PDF file")
            
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def process_document_embeddings(document_id):
    """Process document embeddings asynchronously"""
    try:
        document = Document.objects.get(id=document_id)
        
        # Extract text
        text = extract_text_from_pdf(document.file.path)
        
        # Check if OpenAI API key is configured
        from django.conf import settings
        if not hasattr(settings, 'OPENAI_API_KEY') or settings.OPENAI_API_KEY == 'your-openai-api-key-here':
            # Demo mode - simulate processing
            document.status = 'processed'
            document.embedding_id = f"demo_embedding_{document.id}"
            document.processed_at = timezone.now()
            document.save()
            print(f"Demo mode: Document {document_id} processed successfully (simulated)")
            return f"Document {document_id} processed successfully (demo mode)"
        
        # Real processing with OpenAI
        embeddings = create_embeddings(text)
        embedding_id = store_embeddings(embeddings, document.id)
        
        document.status = 'processed'
        document.embedding_id = embedding_id
        document.processed_at = timezone.now()
        document.save()
        
        return f"Document {document_id} processed successfully"
    except Exception as e:
        # Update document status to failed
        document = Document.objects.get(id=document_id)
        document.status = 'failed'
        document.save()
        raise Exception(f"Error processing document {document_id}: {str(e)}")
