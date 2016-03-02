from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nostromo_db',
        'USER': 'fordesk2',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }

}