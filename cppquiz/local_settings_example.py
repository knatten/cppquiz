from . import settings

settings.SITE_URL = "https://cppquiz.org"
settings.DEBUG = True
settings.ALLOWED_HOSTS += ['127.0.0.1']
settings.ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

settings.DATABASES = {
    'default': {
        # Set to 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle':
        'ENGINE': 'django.db.backends.sqlite3',
        # Database name, or path to database file if using sqlite3:
        'NAME': '/path/to/your/code/cppquiz/db.sqlite3',
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3:
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3:
        'PORT': '',
    }
}

settings.TEMPLATES[0]['DIRS'].append('/path/to/your/code/cppquiz/templates')
settings.TEMPLATES[0]['OPTIONS']['debug'] = True

settings.STATIC_ROOT = ''
settings.STATIC_URL = '/static/'

settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
