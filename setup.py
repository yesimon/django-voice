# -*- coding: utf-8 -*-

import os
import djangovoice
from setuptools import setup, find_packages


setup(
    name='django-voice',
    version=djangovoice.get_version(),
    description="A feedback application for Django 1.3 or later",
    author='Gökmen Görgen',
    author_email='gokmen@alageek.com',
    url='https://github.com/alageek/django-voice',
    license='BSD',
    packages=find_packages(exclude=('demo', 'demo.*')),
    package_data={'djangovoice': ['static/*',
                                  'templates/*']},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment"
    ],
    install_requires=[
        "Django>=1.3",
        "django-gravatar==0.1.0",
        "django-voting==0.1"
    ]
)
