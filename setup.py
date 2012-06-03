# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

djangovoice = __import__('djangovoice')
description = file('README.rst', 'r')

setup(
    name='django-voice',
    version=djangovoice.get_version(),
    description="A feedback application for Django 1.3 or later",
    long_description=description.read(),
    author=u'Gökmen Görgen',
    author_email='gokmen@alageek.com',
    url='https://github.com/gkmngrgn/django-voice',
    license='BSD',
    platforms='any',
    packages=find_packages(exclude=('demo', 'demo.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment"
    ],
    install_requires=[
        "Django>=1.3",
        "django-gravatar>=0.1.0",
        "django-voting>=0.1"
    ]
)
