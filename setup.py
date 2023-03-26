#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="waf-tools",
    version="1.0.0",
    author="Bernardo Fichera",
    author_email="bernardo.fichera@gmail.com",
    description="Collection of Waf Tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nash169/waf-tools.git",
    packages=setuptools.find_packages(),
    scripts=['bin/waf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT LICENSE",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # install_requires=[
    #     "os",
    #     "pathlib",
    # ],
)
