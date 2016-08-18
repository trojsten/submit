#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='submit',
    version='0.0.0',
    packages=[
        'submit',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.9',
        'django-bootstrap-form>=3.2',
        'django-sendfile>=0.3.10',
        'Unidecode>=0.4.19',
    ],
)
