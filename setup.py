#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path


setup(
    name='moulton',
    description='',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pyderman",
        "beautifulsoup4",
        "tqdm",
        "pprint",
        "requests"
    ],
)
