import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key')
    JWT_SECRET = os.environ.get('JWT_SECRET', 'change_this_jwt_secret')
    DB_USER = os.environ.get('DB_USER', 'ashams001')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'iqHired@123')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_NAME = os.environ.get('DB_NAME', 'hd')
    DB_PORT = int(os.environ.get('DB_PORT', 8889))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Theme and branding
    SITE_LOGO = os.environ.get('SITE_LOGO', 'logo.png')
    THEME_COLOR = os.environ.get('THEME_COLOR', '#009688')  # Orange shade
    HEADER_BG = os.environ.get('HEADER_BG', '#fff')
    HEADER_TEXT = os.environ.get('HEADER_TEXT', '#009688')  # Orange shade

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
