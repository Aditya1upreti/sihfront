# app/config/development.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DevelopmentConfig:
    # Basic Flask Configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///agri_assistant.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', 'jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_EXPIRATION_HOURS', 24)) * 3600
    
    # API Keys
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'your-gemini-api-key')
    
    # Application Settings
    APP_NAME = os.environ.get('APP_NAME', 'Krish-Sahayak')
    APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')
    
    # CORS Settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_FILE_SIZE', 16777216))  # 16MB
    
    # Feature Toggles
    WEATHER_FEATURE_ENABLED = os.environ.get('WEATHER_FEATURE_ENABLED', 'true').lower() == 'true'
    MARKET_PRICES_FEATURE_ENABLED = os.environ.get('MARKET_PRICES_FEATURE_ENABLED', 'true').lower() == 'true'
    GRIEVANCES_FEATURE_ENABLED = os.environ.get('GRIEVANCES_FEATURE_ENABLED', 'true').lower() == 'true'
    SUBSIDIES_FEATURE_ENABLED = os.environ.get('SUBSIDIES_FEATURE_ENABLED', 'true').lower() == 'true'
    
    # Security Settings
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')