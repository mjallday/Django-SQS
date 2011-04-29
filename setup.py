#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test


class mytest(test):
    def run(self, *args, **kwargs):
        from runtests import runtests
        runtests()
        # Upgrade().run(dist=True)
        # test.run(self, *args, **kwargs)

setup(
    name='django_sqs',
    version='0.0.1',
    author='Marshall Jones',
    author_email='marshall@offby3.com',
    url='http://github.com/mjallday/Django-SQS',
    description = 'View Amazon AWS SQS Queues in Django',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['boto'],
    test_suite = 'sentry.tests',
    include_package_data=True,
    cmdclass={"test": mytest},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)