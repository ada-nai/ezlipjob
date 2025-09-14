# 🚀 Deployment Guide

This guide covers deploying the LinkedIn Job Application Assistant to Streamlit Cloud and other platforms.

## Table of Contents
- [Quick Start](#quick-start)
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key from [platform.openai.com](https://platform.openai.com)
- Git account for code hosting

### 1-Minute Local Setup
```bash
# Clone and setup
git clone <your-repo-url>
cd linkedin-job-assistant
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure API key
mkdir -p .streamlit
echo '[general]' > .streamlit/secrets.toml
echo 'OPENAI_API_KEY = "your-api-key-here"' >> .streamlit/secrets.toml

# Launch app
streamlit run app.py
```

---

## Streamlit Cloud Deployment

### Step 1: Prepare Repository
1. **Push to GitHub/GitLab**:
   ```bash
   git add .
   git commit -m "LinkedIn Job Assistant ready for deployment"
   git push origin main
   ```

2. **Verify Required Files**:
   - ✅ `app.py` (main application)
   - ✅ `requirements.txt` (dependencies)
   - ✅ `config.py` (configuration manager)
   - ✅ All module files (`content_generator.py`, `resume_processor.py`, etc.)

### Step 2: Deploy to Streamlit Cloud
1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Connect Repository**:
   - Sign in with GitHub/GitLab
   - Select your repository
   - Choose `main` branch
   - Set main file path: `app.py`

3. **Configure Secrets**:
   Click "Advanced settings" → "Secrets" and add:
   ```toml
   [general]
   OPENAI_API_KEY = "sk-your-actual-api-key"
   OPENAI_MODEL = "gpt-4o"
   DEBUG_MODE = "false"
   MAX_FILE_SIZE_MB = "20"
   COVER_LETTER_MAX_WORDS = "350"
   ```

4. **Deploy**:
   - Click "Deploy!"
   - Wait for build completion (~2-3 minutes)
   - Access your live app at the provided URL

### Step 3: Post-Deployment
- **Test all features** with real data
- **Monitor usage** in OpenAI dashboard
- **Set up analytics** (optional)

---

## Local Development

### Development Setup
```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
python -m pytest tests/

# Format code
black *.py

# Type checking
mypy app.py
```

### Environment Configuration
Create `.streamlit/secrets.toml`:
```toml
[general]
# Required
OPENAI_API_KEY = "sk-your-dev-api-key"

# Optional Development Settings
DEBUG_MODE = "true"
OPENAI_MODEL = "gpt-3.5-turbo"  # Cheaper for development
COVER_LETTER_MAX_WORDS = "200"
MAX_FILE_SIZE_MB = "5"

# Development Theme
THEME_PRIMARY_COLOR = "#00D4AA"
```

### Development Workflow
```bash
# Start development server
streamlit run app.py --server.runOnSave true

# In another terminal, watch for changes
python -m pytest tests/ --watch
```

---

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  linkedin-assistant:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=gpt-4o
      - DEBUG_MODE=false
      - MAX_FILE_SIZE_MB=20
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    
  # Optional: Redis for caching
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### Build and Run
```bash
# Build image
docker build -t linkedin-assistant .

# Run with environment file
docker run -p 8501:8501 --env-file .env linkedin-assistant

# Or with docker-compose
docker-compose up -d
```

---

## Environment Configuration

### Production Settings
```bash
# Essential Production Variables
OPENAI_API_KEY=sk-your-production-key
OPENAI_MODEL=gpt-4o
DEBUG_MODE=false

# Performance Tuning
OPENAI_MAX_TOKENS=4000
OPENAI_TIMEOUT=60
REQUESTS_PER_MINUTE=100
MAX_CONCURRENT_REQUESTS=10

# Security
MAX_FILE_SIZE_MB=20
ALLOWED_FILE_TYPES=pdf,docx,txt

# Monitoring
APP_VERSION=1.0.0
```

### High-Traffic Configuration
```bash
# For high-volume usage
OPENAI_MODEL=gpt-4-turbo
REQUESTS_PER_MINUTE=200
MAX_CONCURRENT_REQUESTS=15
SCRAPING_TIMEOUT=15
OPENAI_TIMEOUT=90
```

### Cost Optimization
```bash
# For cost-conscious deployment
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=2000
COVER_LETTER_MAX_WORDS=250
EMAIL_MAX_WORDS=120
```

---

## Platform-Specific Deployments

### Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Configure environment
heroku config:set OPENAI_API_KEY=sk-your-key
heroku config:set OPENAI_MODEL=gpt-4o

# Deploy
git push heroku main
```

### AWS EC2
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Setup application
git clone your-repo
cd linkedin-assistant
pip3 install -r requirements.txt

# Configure systemd service
sudo nano /etc/systemd/system/linkedin-assistant.service

# Start service
sudo systemctl enable linkedin-assistant
sudo systemctl start linkedin-assistant
```

### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/linkedin-assistant
gcloud run deploy --image gcr.io/PROJECT-ID/linkedin-assistant --platform managed
```

---

## Monitoring & Maintenance

### Key Metrics to Monitor
- **OpenAI API Usage**: Tokens, requests, costs
- **Application Performance**: Response times, error rates
- **User Activity**: Active users, feature usage
- **System Resources**: Memory, CPU, storage

### Health Checks
```python
# Add to app.py for monitoring
def health_check():
    """Health check endpoint"""
    try:
        config = get_config()
        return {"status": "healthy", "version": config.app_version}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Logging Configuration
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Not Found
**Error**: `OpenAI API key not configured`
**Solution**:
```bash
# Check environment variables
echo $OPENAI_API_KEY

# Verify Streamlit secrets
cat .streamlit/secrets.toml

# Test configuration
python -c "from config import get_config; print(get_config().openai_api_key)"
```

#### 2. Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'X'`
**Solution**:
```bash
# Reinstall requirements
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 3. File Upload Issues
**Error**: File upload fails or times out
**Solution**:
```bash
# Check file size limits
export MAX_FILE_SIZE_MB=50

# Verify file types
export ALLOWED_FILE_TYPES=pdf,docx,txt,doc
```

#### 4. OpenAI Rate Limits
**Error**: `Rate limit exceeded`
**Solution**:
```bash
# Reduce request rate
export REQUESTS_PER_MINUTE=30

# Use different model
export OPENAI_MODEL=gpt-3.5-turbo
```

#### 5. Memory Issues
**Error**: Out of memory errors
**Solution**:
```bash
# Reduce token limits
export OPENAI_MAX_TOKENS=2000

# Limit concurrent requests
export MAX_CONCURRENT_REQUESTS=3
```

### Debug Mode
Enable detailed logging:
```bash
export DEBUG_MODE=true
streamlit run app.py
```

### Support Resources
- **Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **OpenAI API Docs**: [platform.openai.com/docs](https://platform.openai.com/docs)
- **Project Issues**: Create issue in repository

---

## Success Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] API key configured
- [ ] Requirements.txt updated
- [ ] Environment variables documented
- [ ] Error handling tested

### Post-Deployment
- [ ] Application loads successfully
- [ ] File upload works
- [ ] Resume processing functional
- [ ] Job scraping operational
- [ ] AI generation producing quality content
- [ ] Download features working
- [ ] Mobile responsiveness verified

### Production Readiness
- [ ] Monitoring configured
- [ ] Logging implemented
- [ ] Backup strategy defined
- [ ] Security review completed
- [ ] Performance benchmarks established

---

## Performance Optimization

### Caching
```python
# Add to app.py
@st.cache_data
def cached_content_generation(resume_text, job_text):
    # Cache expensive operations
    pass
```

### Async Operations
```python
# For high-throughput deployments
import asyncio
import aiohttp

async def parallel_processing():
    # Process multiple requests concurrently
    pass
```

### CDN Configuration
For static assets:
```yaml
# cloudflare.yml
rules:
  - pattern: "*.css"
    cache_level: aggressive
  - pattern: "*.js"
    cache_level: aggressive
```

---

🎉 **Congratulations!** Your LinkedIn Job Application Assistant is now ready for production deployment!