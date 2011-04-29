#!/usr/bin/env python
import logging
import sys
from os.path import dirname, abspath, join

logging.getLogger('sentry').addHandler(logging.StreamHandler())

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.sites',

            'django_sqs',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        SITE_ID=1,
    )

from django.test.simple import run_tests

def runtests(*test_args):

    if not test_args:
        test_args = ['django_sqs']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])