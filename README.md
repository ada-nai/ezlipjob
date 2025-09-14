# 🎯 EzLipJob - LinkedIn Job Application Assistant

🚀 **Generate personalized cover letters and emails for your job applications in minutes!**

*The fastest way to create tailored application materials that get noticed by hiring managers.*

---

## 🌟 What is EzLipJob?

EzLipJob is an AI-powered Streamlit application that revolutionizes your job application process. Simply upload your resume and paste a job posting - our advanced AI will analyze both and create personalized, professional application materials that highlight your most relevant experience.

### 🎪 **Live Demo**
Experience EzLipJob in action: Error at Streamlit end during deployment ;(

---

## ✨ Key Features

### 🤖 **AI-Powered Intelligence**
- **GPT-4o Integration**: Latest OpenAI model for superior content generation
- **Smart Experience Matching**: Automatically identifies and highlights relevant experience
- **Context-Aware Writing**: Adapts tone and content based on company culture and job requirements

### 📄 **Flexible Resume Processing**
- **Multiple Input Methods**: PDF upload, Word documents, or manual text entry
- **Enhanced Name Extraction**: Intelligent parsing of candidate information
- **Experience Analysis**: Automatic categorization of skills and experience levels

### � **Advanced Job Analysis**
- **LinkedIn Integration**: Direct URL processing for job postings
- **Enhanced Parsing**: Extracts hiring manager details, contact emails, and suggested subject lines
- **Company Insights**: Automatic organization and location detection
- **Requirement Matching**: Maps your experience to specific job requirements

### 🎨 **Professional Output**
- **Multiple Tone Options**: Professional, Casual, Enthusiastic, and Custom styles
- **Ready-to-Send Emails**: Properly formatted with subject lines and contact details
- **Cover Letter Generation**: Tailored documents highlighting your best matches
- **Experience Match Scoring**: Visual relevance indicators (0-100% match confidence)

### ⚡ **Lightning Fast**
- **Under 60 Seconds**: Complete application package generation
- **Real-time Progress**: Live updates during processing
- **Instant Copy**: One-click copying for immediate use

---

## Sample screenshot 
<img width="1915" height="1060" alt="image" src="https://github.com/user-attachments/assets/59e7c51b-6999-490a-8d26-fac47b30f232" />


### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd linkedin-job-assistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a `.streamlit/secrets.toml` file with your OpenAI API key:
```toml
[general]
OPENAI_API_KEY = "your-openai-api-key-here"
OPENAI_MODEL = "gpt-4o"
DEBUG_MODE = "false"
```

**Get your OpenAI API key**: Visit [platform.openai.com](https://platform.openai.com/api-keys)

### 3. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 4. Deploy to Streamlit Cloud
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add your OpenAI API key in "Advanced settings" → "Secrets"
5. Deploy and share your live application!

### Cloud Deployment (Streamlit Cloud)

1. **Fork this repository**
2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
3. **Add secrets**
   - In Streamlit Cloud, add your OpenAI API key to secrets
   - Format: `OPENAI_API_KEY = "your-key-here"`
4. **Deploy**
   - Your app will be available at a public URL

## Usage

1. **Input Resume**: Upload PDF/DOCX or paste text
2. **Add Job Info**: Paste LinkedIn URL or enter manually
3. **Select Tone**: Choose Professional, Warm, or Concise
4. **Generate**: Click to create personalized materials
5. **Copy & Send**: Use the generated content for your applications

## Requirements

### Core Dependencies
- `streamlit>=1.28.0` - Web application framework
- `openai>=1.3.0` - AI content generation
- `PyPDF2>=3.0.1` - PDF text extraction
- `python-docx>=0.8.11` - Word document processing
- `beautifulsoup4>=4.12.2` - Web scraping
- `requests>=2.31.0` - HTTP requests
- `pandas>=2.1.0` - Data manipulation

### API Requirements
- OpenAI API key (required for content generation)
- Internet connection for LinkedIn scraping

## Project Structure

```
job-assistant/
├── app.py                 # Main Streamlit application
├── resume_processor.py    # Resume parsing functions
├── job_scraper.py        # LinkedIn scraping functions
├── content_generator.py  # AI content generation
├── requirements.txt      # Dependencies
├── README.md            # This file
├── .gitignore          # Git ignore rules
└── .streamlit/
    ├── config.toml     # App configuration
    └── secrets.toml    # API keys (local only)
```

## Features & Specifications

### Input Processing
- **Resume Formats**: PDF, DOCX, plain text
- **Job Sources**: LinkedIn URLs, manual input
- **Content Limits**: 200-300 words (cover letter), 100-150 words (email)

### AI Generation
- **Personalization**: Matches experience with job requirements
- **Company Research**: Incorporates company-specific information
- **Professional Standards**: Maintains business communication quality
- **Tone Options**: Adaptable to different company cultures

### Privacy & Security
- **No Data Storage**: Session-based processing only
- **Secure API Keys**: Stored in Streamlit secrets
- **Input Validation**: Sanitizes all user inputs
- **Error Handling**: Graceful fallbacks for all scenarios

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure OpenAI API key is correctly set in secrets
   - Check for sufficient API credits

2. **File Upload Issues**
   - Supported formats: PDF, DOCX only
   - Maximum file size: 10MB
   - Try manual text input as fallback

3. **LinkedIn Scraping Fails**
   - Use manual job details input
   - Check URL format and accessibility

4. **Generation Quality**
   - Ensure resume has sufficient detail
   - Try different tone options
   - Regenerate if content seems generic

### Performance Tips
- Use concise resume text for faster processing
- Valid LinkedIn URLs improve job matching
- Review generated content before sending

## 📚 Documentation

- **[Environment Variables Guide](ENVIRONMENT_VARIABLES.md)** - Complete configuration options
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Production deployment instructions  
- **[Project Summary](PROJECT_SUMMARY.md)** - Implementation details and testing checklist

## 🎯 Project Status

✅ **COMPLETE** - All features implemented and tested
- **Implementation Time**: ~2.5 hours
- **Production Ready**: Yes
- **Documentation**: Comprehensive
- **Testing**: All modules validated

### What's Included:
- 🏗️ **Complete application** with professional UI
- 🤖 **GPT-4o integration** with structured outputs
- 📄 **Multi-format resume processing** (PDF, DOCX, text)
- 🔗 **LinkedIn job scraping** with manual fallback
- ⚙️ **Comprehensive configuration system**
- 🛡️ **Error handling and validation**
- 📖 **Deployment documentation**

## 💡 Next Steps

1. **Set your OpenAI API key** in environment variables
2. **Test locally** with sample resume and job data
3. **Deploy to Streamlit Cloud** for public access
4. **Monitor usage** and gather user feedback

## 📞 Support

For questions, issues, or feature requests:
- Create an issue in this repository
- Review the comprehensive documentation files
- Check the troubleshooting section in the deployment guide

---

🎉 **Ready to transform your job application process with AI!**

**⚠️ Important**: Always review generated content before sending. This tool assists with drafting but human review ensures quality and accuracy.

---

## 📞 Support & Contributing

Found a bug or have a feature request? 
- 🐛 [Report Issues](https://github.com/ada-nai/ezlipjob/issues)
- 💡 [Feature Requests](https://github.com/ada-nai/ezlipjob/discussions)
- 🤝 [Contributing Guidelines](CONTRIBUTING.md)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for job seekers everywhere**
