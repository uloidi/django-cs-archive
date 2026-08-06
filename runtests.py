import os
import sys
import tempfile
import shutil

# Gehitu src direktorioa Python bidera (sys.path) paketea kargatu ahal izateko
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import django
from django.conf import settings

def runtests():
    # Create a temporary directory for templates and write base.html
    temp_dir = tempfile.mkdtemp()
    templates_dir = os.path.join(temp_dir, 'templates')
    os.makedirs(templates_dir)
    
    with open(os.path.join(templates_dir, 'base.html'), 'w') as f:
        f.write('{% block content %}{% endblock %}')

    try:
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
                    'DIRS': [templates_dir],
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
            USE_TZ=True,
            TIME_ZONE='UTC',
        )
        django.setup()
        from django.test.runner import DiscoverRunner
        test_runner = DiscoverRunner(verbosity=1)
        failures = test_runner.run_tests(['django_cs_archive'])
        sys.exit(bool(failures))
    finally:
        # Clean up the temporary templates directory
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    runtests()
