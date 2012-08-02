# -*- coding: utf-8 -*-
"""
Makes requests by Kenneth Reitz a little more magical.
"""

from setuptools import setup

setup(
    name='magicrequests',
    version='0.1.0',
    url='https://github.com/mattseh/magicrequests/tarball/master',
    license='BSD',
    author='Matthew Bell',
    author_email='matthewrobertbell@gmail.com',
    description='Requests + Magic',
    long_description=__doc__,
    py_modules=['magicrequests'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
