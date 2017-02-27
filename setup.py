#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-trojsten-submit',
    packages=[
        'submit',
    ],
    version='0.1.0',
    description='Django app for storing submits and reviews, used in Trojsten seminary web apps',
    author='Mário Lipovský',
    author_email='mario.lipovsky@trojsten.sk',
    url='https://github.com/trojsten/submit',
    include_package_data=True,
    install_requires=[
        'Django>=1.9',
        'django-bootstrap-form>=3.2',
        'django-sendfile>=0.3.10',
        'Unidecode>=0.4.19',
        'djangorestframework>=3.5.4',
    ],
    download_url = 'https://github.com/trojsten/submit/tarball/0.1',
    keywords = ['submit', 'review'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    license='BSD',
)
