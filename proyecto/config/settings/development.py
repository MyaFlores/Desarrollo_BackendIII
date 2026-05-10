from .base import *

DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Base de datos para desarrollo (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

