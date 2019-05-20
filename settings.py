# Django settings for silverbb project.

DEBUG = True
#TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

SYSTEMMAIL = 'noreply@silver-boards.com'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'silverbb',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'hisoka999',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'TEST':{
            'NAME' : 'silverbbtest',
        }
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

ugettext = lambda s: s

LANGUAGES = (
    ('de', ugettext('German')),
    ('en', ugettext('English')),
)


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True
import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT =  PROJECT_ROOT+'/media'
STATICFILES_DIRS = (
    PROJECT_ROOT+"/static",
)
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static_media/'

STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '31w689-k)zz^u26$q+^apj&w-yfr$y0ordfxa0j^nnww^#@%m&'


MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'users.middleware.UserMiddleware'
)
ROOT_URLCONF = 'urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_ROOT+"/templates",
        ],
        #'APP_DIRS': True,
        'OPTIONS': {
            'debug':DEBUG,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'backend.context_processors.theme_path',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.user_auth',
                'backend.context_processors.version',
                'msg.context_processors.msg_stats',
                
                'cms.context_processors.menu'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',    
            ],
        },
    },
]


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'board',
    'users',
    'backend',
    'faq',
    'msg',
    'cms',
    'blog'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/django_debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True
FIXTURE_DIRS = (
    'fixtures',
)
LOCALE_PATHS = [
    'locale'
]

# User Profile
AUTH_PROFILE_MODULE = "users.UserProfile"
