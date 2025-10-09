import os
import uuid
import numpy as np
from django.conf import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import openai

# Initialize OpenAI
openai.api_key = settings.OPENAI_API_KEY

def create_embeddings(text):
    """Create embeddings for text using OpenAI"""
    try:
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        
        # Create embeddings
        embeddings = OpenAIEmbeddings()
        return chunks, embeddings
    except Exception as e:
        raise Exception(f"Error creating embeddings: {str(e)}")

def store_embeddings(embeddings_data, document_id):
    """Store embeddings in FAISS vector store"""
    try:
        chunks, embeddings = embeddings_data
        
        # Create FAISS vector store
        vectorstore = FAISS.from_texts(chunks, embeddings)
        
        # Save vector store
        embedding_id = str(uuid.uuid4())
        embeddings_dir = os.path.join(settings.MEDIA_ROOT, 'embeddings')
        os.makedirs(embeddings_dir, exist_ok=True)
        vectorstore.save_local(embeddings_dir, index_name=embedding_id)
        
        return embedding_id
    except Exception as e:
        raise Exception(f"Error storing embeddings: {str(e)}")

def load_embeddings(embedding_id):
    """Load embeddings from FAISS vector store"""
    try:
        embeddings_dir = os.path.join(settings.MEDIA_ROOT, 'embeddings')
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(embeddings_dir, embeddings, index_name=embedding_id, allow_dangerous_deserialization=True)
        return vectorstore
    except Exception as e:
        raise Exception(f"Error loading embeddings: {str(e)}")

def get_ai_response(query, document_id):
    """Get AI response using RAG"""
    try:
        # Check if OpenAI API key is properly configured
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
            return get_ai_response_demo(query, document_id)
        
        # Check if it's a placeholder or invalid key
        key = settings.OPENAI_API_KEY.strip()
        if (key == 'your-openai-api-key-here' or 
            key == 'key_here' or 
            key == '' or  # Empty string
            not key.startswith('sk-') or 
            len(key) < 20):
            return get_ai_response_demo(query, document_id)
        
        # Load document embeddings
        vectorstore = load_embeddings(document_id)
        
        # Create QA chain
        llm = OpenAI(temperature=0.7)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 4})
        )
        
        # Get response
        response = qa_chain.run(query)
        return response
    except Exception as e:
        raise Exception(f"Error getting AI response: {str(e)}")

def get_ai_response_demo(query, document_id):
    """Demo mode AI response for testing without OpenAI API"""
    demo_responses = [
        f"I understand you're asking about: '{query}'. This is a demo response since no OpenAI API key is configured. In the full version, I would analyze your document and provide detailed answers based on the content.",
        f"Great question! '{query}' - In demo mode, I can't access the actual document content, but I would normally search through your uploaded document to find relevant information and provide a comprehensive answer.",
        f"Regarding '{query}' - This is a simulated response. With a proper OpenAI API key, I would use RAG (Retrieval-Augmented Generation) to find the most relevant parts of your document and generate accurate answers.",
        f"Your question '{query}' is interesting! In the full version, I would use vector similarity search to find the most relevant sections of your document and provide detailed, contextual answers.",
    ]
    
    import random
    return random.choice(demo_responses)
