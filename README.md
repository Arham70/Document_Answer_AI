# DocuMind - AI Document Q&A System

A beautiful, responsive Django web application where users can register, upload PDFs, chat with AI about their uploaded documents, manage their profiles, and export chat history as downloadable .docx files.

## Features

- 🎨 **Beautiful UI**: Modern design with TailwindCSS and glassmorphism effects
- 📄 **PDF Processing**: Upload and process PDF documents with AI
- 🤖 **AI Chat**: Chat with AI about your documents using RAG (Retrieval-Augmented Generation)
- 👤 **User Management**: Complete authentication system with profile management
- 📊 **Dashboard**: User-friendly dashboard to manage documents and chats
- 📥 **Export**: Export chat conversations as professional DOCX files
- 🔒 **Secure**: User isolation and secure document handling
- 📱 **Responsive**: Works perfectly on desktop, tablet, and mobile

## Tech Stack

- **Backend**: Django 5.x
- **Frontend**: Django Templates + TailwindCSS
- **Database**: PostgreSQL (production) / SQLite (development)
- **AI & RAG**: LangChain + FAISS/ChromaDB
- **LLM**: OpenAI GPT API
- **File Processing**: PyMuPDF
- **Export**: python-docx
- **Deployment**: Render (Free Tier)

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key

### Virtual Environment Setup

**Important**: Always use a virtual environment to avoid dependency conflicts!

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Verify activation (should show venv path)
which python  # macOS/Linux
where python  # Windows
```

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Document_Answer_AI
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open http://127.0.0.1:8000 in your browser
   - Register a new account or use admin credentials

## Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/documind

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Usage

### For Users

1. **Register**: Create a new account
2. **Upload**: Upload PDF documents (max 10MB)
3. **Wait**: Documents are processed automatically
4. **Chat**: Start conversations with AI about your documents
5. **Export**: Download chat conversations as DOCX files

### For Developers

1. **Admin Panel**: Access at `/admin/` with superuser credentials
2. **API**: RESTful API endpoints for document and chat management
3. **Customization**: Modify templates, add new features, integrate additional AI models

## Deployment

### Render (Recommended)

1. **Connect Repository**: Link your GitHub repository to Render
2. **Set Environment Variables**: Add all required environment variables
3. **Deploy**: Render will automatically build and deploy your application

### Manual Deployment

1. **Prepare Production Settings**:
   ```bash
   python manage.py collectstatic
   python manage.py migrate
   ```

2. **Use Production Server**:
   ```bash
   gunicorn documind.wsgi:application
   ```

## Project Structure

```
Document_Answer_AI/
├── documind/                 # Django project settings
├── core/                     # Core app (landing page, dashboard)
├── accounts/                 # User authentication
├── documents/                # Document management
├── chat/                     # Chat functionality
├── templates/                # HTML templates
├── static/                   # Static files
├── media/                    # User uploads
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment configuration
└── README.md                 # This file
```

## API Endpoints

- `GET /` - Landing page
- `GET /dashboard/` - User dashboard
- `POST /documents/upload/` - Upload document
- `GET /chat/<id>/` - Chat interface
- `POST /chat/<id>/send/` - Send message
- `GET /chat/<id>/export/` - Export chat

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, email support@documind.ai or create an issue in the repository.

## Roadmap

- [ ] Multi-document chat
- [ ] Document summarization
- [ ] Advanced analytics
- [ ] API rate limiting
- [ ] Mobile app
- [ ] Integration with cloud storage

---

Built with ❤️ using Django and AI