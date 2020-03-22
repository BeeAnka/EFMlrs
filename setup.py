"""A setuptools based setup module for EFMlrs"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # NOTE: put package requirements here
    'cobra==0.17.1',
    'numpy==1.18.1',
    'pandas==1.0.1',
    'sympy==1.5.1',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='efmlrs',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Extracts EFMs from result file of mplrs and decompresses EFMs from efmtool and mplrs results that have been compressed with EFMlrs",
    long_description=readme + '\n\n' + history,
    author="Bianca Buchner",
    author_email='bianca.buchner@gmail.com',
    url='https://github.com/BeeAnka/EFMlrs',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts':[
            'efmlrs_pre=efmlrs.pre:start_from_command_line',
            'efmlrs_post=efmlrs.post:start_from_command_line'
            ],
        },
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        #'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
