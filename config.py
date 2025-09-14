"""
Configuration and Environment Variable Management
Handles loading environment variables from multiple sources with fallbacks
"""

import os
import streamlit as st
from typing import Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppConfig:
    """Application configuration with environment variables"""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o"
    openai_max_tokens: int = 4000
    openai_temperature: float = 0.7
    openai_timeout: int = 60
    
    # Application Settings
    app_name: str = "LinkedIn Job Application Assistant"
    app_version: str = "1.0.0"
    debug_mode: bool = False
    
    # Content Generation Settings
    cover_letter_min_words: int = 200
    cover_letter_max_words: int = 300
    email_min_words: int = 100
    email_max_words: int = 150
    
    # LinkedIn Scraping Settings
    scraping_timeout: int = 10
    scraping_delay: float = 1.0
    max_retries: int = 3
    
    # Rate Limiting
    requests_per_minute: int = 60
    max_concurrent_requests: int = 5
    
    # File Upload Settings
    max_file_size_mb: int = 10
    allowed_file_types: list = None
    
    # UI Settings
    theme_primary_color: str = "#FF6B6B"
    theme_background_color: str = "#FFFFFF"
    theme_secondary_background: str = "#F0F2F6"
    theme_text_color: str = "#262730"
    
    def __post_init__(self):
        if self.allowed_file_types is None:
            self.allowed_file_types = ["pdf", "docx", "txt"]

class ConfigManager:
    """Manages configuration loading from multiple sources"""
    
    def __init__(self):
        self.config = None
        self._load_config()
    
    def _get_env_var(self, key: str, default: Any = None, var_type: type = str) -> Any:
        """Get environment variable with type conversion and fallbacks"""
        
        # Priority order: OS environment -> Streamlit secrets -> default
        value = None
        
        # 1. Try OS environment variables
        if key in os.environ:
            value = os.environ[key]
            
        # 2. Try Streamlit secrets
        elif hasattr(st, 'secrets'):
            try:
                # Check in general section first
                if 'general' in st.secrets and key in st.secrets['general']:
                    value = st.secrets['general'][key]
                # Check in root level
                elif key in st.secrets:
                    value = st.secrets[key]
            except Exception:
                pass
        
        # 3. Use default
        if value is None:
            return default
        
        # Type conversion
        if var_type == bool:
            return str(value).lower() in ('true', '1', 'yes', 'on')
        elif var_type == int:
            try:
                return int(value)
            except ValueError:
                return default
        elif var_type == float:
            try:
                return float(value)
            except ValueError:
                return default
        elif var_type == list:
            if isinstance(value, str):
                return [item.strip() for item in value.split(',')]
            return value
        
        return str(value)
    
    def _load_config(self):
        """Load configuration from all sources"""
        
        # Load OpenAI settings
        openai_api_key = self._get_env_var('OPENAI_API_KEY')
        if not openai_api_key or openai_api_key == "your-openai-api-key-here":
            raise ValueError(
                "OpenAI API key not configured. Set OPENAI_API_KEY environment variable "
                "or add to Streamlit secrets."
            )
        
        self.config = AppConfig(
            # OpenAI Configuration
            openai_api_key=openai_api_key,
            openai_model=self._get_env_var('OPENAI_MODEL', 'gpt-4o'),
            openai_max_tokens=self._get_env_var('OPENAI_MAX_TOKENS', 4000, int),
            openai_temperature=self._get_env_var('OPENAI_TEMPERATURE', 0.7, float),
            openai_timeout=self._get_env_var('OPENAI_TIMEOUT', 60, int),
            
            # Application Settings
            app_name=self._get_env_var('APP_NAME', 'LinkedIn Job Application Assistant'),
            app_version=self._get_env_var('APP_VERSION', '1.0.0'),
            debug_mode=self._get_env_var('DEBUG_MODE', False, bool),
            
            # Content Generation Settings
            cover_letter_min_words=self._get_env_var('COVER_LETTER_MIN_WORDS', 200, int),
            cover_letter_max_words=self._get_env_var('COVER_LETTER_MAX_WORDS', 300, int),
            email_min_words=self._get_env_var('EMAIL_MIN_WORDS', 100, int),
            email_max_words=self._get_env_var('EMAIL_MAX_WORDS', 150, int),
            
            # LinkedIn Scraping Settings
            scraping_timeout=self._get_env_var('SCRAPING_TIMEOUT', 10, int),
            scraping_delay=self._get_env_var('SCRAPING_DELAY', 1.0, float),
            max_retries=self._get_env_var('MAX_RETRIES', 3, int),
            
            # Rate Limiting
            requests_per_minute=self._get_env_var('REQUESTS_PER_MINUTE', 60, int),
            max_concurrent_requests=self._get_env_var('MAX_CONCURRENT_REQUESTS', 5, int),
            
            # File Upload Settings
            max_file_size_mb=self._get_env_var('MAX_FILE_SIZE_MB', 10, int),
            allowed_file_types=self._get_env_var('ALLOWED_FILE_TYPES', ['pdf', 'docx', 'txt'], list),
            
            # UI Theme Settings
            theme_primary_color=self._get_env_var('THEME_PRIMARY_COLOR', '#FF6B6B'),
            theme_background_color=self._get_env_var('THEME_BACKGROUND_COLOR', '#FFFFFF'),
            theme_secondary_background=self._get_env_var('THEME_SECONDARY_BACKGROUND', '#F0F2F6'),
            theme_text_color=self._get_env_var('THEME_TEXT_COLOR', '#262730')
        )
    
    def get_config(self) -> AppConfig:
        """Get the loaded configuration"""
        if self.config is None:
            self._load_config()
        return self.config
    
    def validate_config(self) -> tuple[bool, list[str]]:
        """Validate configuration and return status with any errors"""
        errors = []
        
        config = self.get_config()
        
        # Validate OpenAI API key
        if not config.openai_api_key:
            errors.append("OpenAI API key is required")
        
        # Validate numeric ranges
        if config.openai_max_tokens < 100:
            errors.append("OpenAI max tokens must be at least 100")
        
        if config.cover_letter_min_words >= config.cover_letter_max_words:
            errors.append("Cover letter min words must be less than max words")
        
        if config.email_min_words >= config.email_max_words:
            errors.append("Email min words must be less than max words")
        
        if config.max_file_size_mb < 1:
            errors.append("Max file size must be at least 1MB")
        
        return len(errors) == 0, errors
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get debug information about configuration sources"""
        config = self.get_config()
        
        debug_info = {
            'config_values': {
                'openai_model': config.openai_model,
                'openai_max_tokens': config.openai_max_tokens,
                'openai_temperature': config.openai_temperature,
                'debug_mode': config.debug_mode,
                'app_version': config.app_version,
                'max_file_size_mb': config.max_file_size_mb,
                'allowed_file_types': config.allowed_file_types
            },
            'environment_sources': {
                'os_env_vars': [key for key in os.environ.keys() if 'OPENAI' in key or 'APP_' in key],
                'streamlit_secrets_available': hasattr(st, 'secrets'),
                'config_file_exists': Path('.streamlit/secrets.toml').exists()
            }
        }
        
        return debug_info

# Global configuration manager instance
_config_manager = None

def get_config() -> AppConfig:
    """Get the global application configuration"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.get_config()

def validate_configuration() -> tuple[bool, list[str]]:
    """Validate the current configuration"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.validate_config()

def get_debug_info() -> Dict[str, Any]:
    """Get configuration debug information"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.get_debug_info()

def reload_config():
    """Reload configuration from environment"""
    global _config_manager
    _config_manager = None
    return get_config()

# Convenience functions for common config access
def get_openai_config() -> dict:
    """Get OpenAI-specific configuration"""
    config = get_config()
    return {
        'api_key': config.openai_api_key,
        'model': config.openai_model,
        'max_tokens': config.openai_max_tokens,
        'temperature': config.openai_temperature,
        'timeout': config.openai_timeout
    }

def get_content_limits() -> dict:
    """Get content generation limits"""
    config = get_config()
    return {
        'cover_letter_min': config.cover_letter_min_words,
        'cover_letter_max': config.cover_letter_max_words,
        'email_min': config.email_min_words,
        'email_max': config.email_max_words
    }

def get_upload_settings() -> dict:
    """Get file upload settings"""
    config = get_config()
    return {
        'max_size_mb': config.max_file_size_mb,
        'allowed_types': config.allowed_file_types
    }