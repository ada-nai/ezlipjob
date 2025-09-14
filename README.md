# LinkedIn Job Application Assistant

🚀 **Generate personalized cover letters and emails for your job applications in minutes!**

## Overview

This Streamlit application helps job seekers create personalized cover letters and professional emails by analyzing their resume and LinkedIn job postings. The app uses AI to match candidate experience with job requirements and generates tailored application materials.

## Features

- 📄 **Resume Processing**: Upload PDF/DOCX files or paste resume text
- 🔗 **LinkedIn Integration**: Extract job details from LinkedIn URLs
- 🤖 **AI-Powered Generation**: Create personalized cover letters and emails
- 🎨 **Tone Variations**: Professional, Warm, or Concise styles
- 📧 **Ready-to-Send**: Formatted email drafts with copy functionality
- ⚡ **Fast Processing**: Generate materials in under 60 seconds

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd job-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Add it to `.streamlit/secrets.toml`:
     ```toml
     [general]
     OPENAI_API_KEY = "your-api-key-here"
     ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review error messages for guidance
- Ensure all requirements are met

---

**⚠️ Important**: Always review generated content before sending. This tool assists with drafting but human review ensures quality and accuracy.