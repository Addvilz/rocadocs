#!/usr/bin/env python

from __future__ import with_statement

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='Roca',
    version="0.0.2",
    description='Opinionated static documentation generator using Markdown',
    long_description=readme,
    author='Addvilz',
    author_email='mrtreinis@gmail.com',
    url='https://github.com/Addvilz/roca',
    download_url='https://github.com/Addvilz/roca',
    license='Apache 2.0',
    platforms='UNIX',
    packages=find_packages(),
    install_requires=[
        "py-gfm>=0.1.3",
        "pygments>=2.1.3",
        "python-slugify>=1.2.1"
    ],
    entry_points={
        'console_scripts': [
            'roca = roca.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: System :: Software Distribution'
    ],
)
