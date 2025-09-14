# Environment Variables Configuration

This document explains all environment variables available in the LinkedIn Job Application Assistant.

## Configuration Methods

The application supports multiple ways to configure environment variables:

### 1. **Streamlit Secrets** (Recommended for local development)
Create `.streamlit/secrets.toml`:
```toml
[general]
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4o"
DEBUG_MODE = "true"
```

### 2. **Environment Variables** (Recommended for production)
Set system environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4o"
export MAX_FILE_SIZE_MB="20"
```

### 3. **Docker Environment**
In docker-compose.yml:
```yaml
environment:
  - OPENAI_API_KEY=sk-...
  - OPENAI_MODEL=gpt-4o
  - DEBUG_MODE=false
```

### 4. **Streamlit Cloud**
Add variables in the Streamlit Cloud dashboard under "Advanced settings" → "Secrets":
```toml
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4o"
```

## Priority Order

Variables are loaded in this priority (highest to lowest):
1. **System Environment Variables** (OS level)
2. **Streamlit Secrets** (`.streamlit/secrets.toml`)
3. **Default Values** (hardcoded fallbacks)

## Available Variables

### 🤖 OpenAI Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *Required* | Your OpenAI API key from platform.openai.com |
| `OPENAI_MODEL` | `gpt-4o` | OpenAI model to use (gpt-4o, gpt-4-turbo, gpt-3.5-turbo) |
| `OPENAI_MAX_TOKENS` | `4000` | Maximum tokens per API request |
| `OPENAI_TEMPERATURE` | `0.7` | Creativity level (0.0-1.0) |
| `OPENAI_TIMEOUT` | `60` | API request timeout in seconds |

### 📱 Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `LinkedIn Job Application Assistant` | Application display name |
| `APP_VERSION` | `1.0.0` | Version number |
| `DEBUG_MODE` | `false` | Enable debug information and logs |

### 📝 Content Generation

| Variable | Default | Description |
|----------|---------|-------------|
| `COVER_LETTER_MIN_WORDS` | `200` | Minimum words for cover letters |
| `COVER_LETTER_MAX_WORDS` | `300` | Maximum words for cover letters |
| `EMAIL_MIN_WORDS` | `100` | Minimum words for email body |
| `EMAIL_MAX_WORDS` | `150` | Maximum words for email body |

### 🔗 LinkedIn Scraping

| Variable | Default | Description |
|----------|---------|-------------|
| `SCRAPING_TIMEOUT` | `10` | Timeout for web scraping requests (seconds) |
| `SCRAPING_DELAY` | `1.0` | Delay between requests to avoid rate limiting |
| `MAX_RETRIES` | `3` | Maximum retry attempts for failed requests |

### ⚡ Rate Limiting

| Variable | Default | Description |
|----------|---------|-------------|
| `REQUESTS_PER_MINUTE` | `60` | Maximum requests per minute |
| `MAX_CONCURRENT_REQUESTS` | `5` | Maximum concurrent API requests |

### 📁 File Upload

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_FILE_SIZE_MB` | `10` | Maximum upload file size in megabytes |
| `ALLOWED_FILE_TYPES` | `pdf,docx,txt` | Comma-separated list of allowed file extensions |

### 🎨 UI Theme

| Variable | Default | Description |
|----------|---------|-------------|
| `THEME_PRIMARY_COLOR` | `#FF6B6B` | Primary color for buttons and highlights |
| `THEME_BACKGROUND_COLOR` | `#FFFFFF` | Main background color |
| `THEME_SECONDARY_BACKGROUND` | `#F0F2F6` | Secondary background color |
| `THEME_TEXT_COLOR` | `#262730` | Main text color |

## Example Configurations

### Development Setup
```toml
# .streamlit/secrets.toml
[general]
OPENAI_API_KEY = "sk-your-dev-key"
OPENAI_MODEL = "gpt-4o"
DEBUG_MODE = "true"
COVER_LETTER_MAX_WORDS = "250"
MAX_FILE_SIZE_MB = "5"
```

### Production Setup
```bash
# Environment variables
export OPENAI_API_KEY="sk-your-prod-key"
export OPENAI_MODEL="gpt-4o"
export DEBUG_MODE="false"
export COVER_LETTER_MIN_WORDS="200"
export COVER_LETTER_MAX_WORDS="300"
export MAX_FILE_SIZE_MB="20"
export REQUESTS_PER_MINUTE="100"
```

### High-Volume Setup
```bash
# For high-traffic deployments
export OPENAI_MODEL="gpt-4-turbo"
export OPENAI_MAX_TOKENS="2000"
export REQUESTS_PER_MINUTE="200"
export MAX_CONCURRENT_REQUESTS="10"
export SCRAPING_TIMEOUT="15"
```

## Validation

The application validates all configuration on startup and will show clear error messages for:
- Missing required variables (OPENAI_API_KEY)
- Invalid value ranges (negative numbers, etc.)
- Malformed configuration

## Environment-Specific Tips

### Local Development
- Use `.streamlit/secrets.toml` for convenience
- Enable `DEBUG_MODE=true` to see configuration details
- Use smaller limits for testing

### Streamlit Cloud
- Add secrets in the dashboard
- Use production values
- Monitor usage against OpenAI limits

### Docker Deployment
- Use environment variables in compose file
- Consider using secrets management
- Set appropriate resource limits

### Enterprise Deployment
- Use dedicated API keys with higher limits
- Configure appropriate rate limiting
- Enable monitoring and logging
- Consider cost management settings

## Security Notes

- ⚠️ **Never commit API keys to version control**
- 🔒 Use secrets management in production
- 🔄 Rotate API keys regularly
- 📊 Monitor API usage and costs
- 🛡️ Use environment-specific keys (dev/staging/prod)