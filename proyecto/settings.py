# proyecto/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-mn05h8*f2i9nd%h!eboh&*38d*4_(&z_3-0jgwp6e+&y%ko=k5'
DEBUG = True
ALLOWED_HOSTS = []

# APLICACIONES
INSTALLED_APPS = [
    'daphne',  # PRIMERO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # TERCEROS
    'channels',
    'tailwind',
    'theme',
    'django_browser_reload',
    'widget_tweaks',
    'rest_framework',
    
    # MIS APPS
    'blog',
    'products',
    'users',
    'games',
    'api_errors',
    'ApisExternasApp',
    'chatbot',
]

# CHANNELS - WEBSOCKETS
ASGI_APPLICATION = 'proyecto.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],  
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'proyecto.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'proyecto', 'templates'),
            os.path.join(BASE_DIR, 'theme', 'templates'), 
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# STATIC Y MEDIA - ✅ CORREGIDO
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'proyecto' / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# TAILWIND
TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

# LOGIN
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/games/'
LOGOUT_REDIRECT_URL = '/users/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'