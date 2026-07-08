import os
from datetime import timedelta

class Config:
    """Temel Konfigürasyon"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'morphex-ai-secret-key-2026')
    DEBUG = os.getenv('DEBUG', False)
    
class DevelopmentConfig(Config):
    """Geliştirme Ortamı"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///morphex_ai.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-morphex')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

class ProductionConfig(Config):
    """Üretim Ortamı"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///morphex_ai.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
