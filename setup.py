# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 00:23:29 2018

@author: khanhphamdinh
"""
from setuptools import setup, find_packages

# All metadata is now in pyproject.toml
setup(
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    zip_safe=False,
)
