import os
import sys

# Gehitu src direktorioa Python bidera (sys.path) paketea kargatu ahal izateko
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import django
from django.conf import settings

def runtests():
    # Configure minimum settings required to test django_cs_archive
    settings.configure(
        DEBUG=True,
        SECRET_KEY='dummy_secret_key_for_testing_purposes',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django_cs_archive',
        ],
        CS_ARCHIVE_MODEL='django_cs_archive.TestArticle',
        CS_ARCHIVE_DATE_FIELD='pub_date',
        ROOT_URLCONF='django_cs_archive.tests',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': ['/tmp/opencode/templates'],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                    ],
                },
            },
        ],
        MIDDLEWARE=[
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ],
        USE_TZ=False,
        TIME_ZONE='UTC',
    )
    django.setup()
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(verbosity=1)
    failures = test_runner.run_tests(['django_cs_archive'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
