#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='requests-jwt',
    version='0.5.3',
    url='https://github.com/tgs/requests-jwt',
    py_modules=['requests_jwt'],
    install_requires=[ 'requests', 'PyJWT' ],
    tests_require=['httpretty'],
    test_suite='tests.suite',
    provides=[ 'requests_jwt' ],
    author='Thomas Grenfell Smith',
    author_email='thomathom@gmail.com',
    description='This package allows for HTTP JSON Web Token (JWT) authentication using the requests library.',
    long_description=open('README.rst').read(),
    license='ISC',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
)
