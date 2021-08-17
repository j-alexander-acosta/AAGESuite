from .base import *  # noqa

DEVELOPMENT_APPS = []

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS + DEVELOPMENT_APPS

ALLOWED_HOSTS = ['*']

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
COMPRESS_CSS_HASHING_METHOD = 'content'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
