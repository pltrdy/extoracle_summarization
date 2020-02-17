#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='extoracle',
    description='Ext-Oracle Summarization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1',
    packages=find_packages(),
    project_urls={
        "Source": "https://github.com/pltrdy/extoracle_summarization/"
    },
    install_requires=[
        "rouge>=1.0.0rc1"
    ],
    entry_points={
        "console_scripts": [
            "extoracle=extoracle.bin.cmd:main",
        ],
    }
)
