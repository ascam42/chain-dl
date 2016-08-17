#!/usr/bin/env python3
"""
    A simple chained videos downloader.
    Using the awesome youtube-dl !

    Author: Luca Ungaro <luca.ungaro@hotmail.fr>
    git: https://github.com/ascam42/chain-dl
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme:
    long_description = readme.read()

setup(
        name="chain-dl",
        version="1.0.0",

        description="A simple chained videos downloader using the awesome youtube-dl",
        long_description=long_description,

        url="https://github.com/ascam42/chain-dl",

        author="Luca Ungaro",
        author_email="luca.ungaro@hotmail.fr",

        license="MIT",

        classifiers=[
            'Development Status :: 4 - Beta',
            'Topic :: Multimedia :: Video',
            'Environment :: Console',

            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',

            'Operating System :: Unix',
            'Programming Language :: Python :: 3 :: Only'
        ],

        keywords="chain video download",

        # packages=[
            # 'bs4',
            # 'llvm'
        # ] + find_packages(),
        packages=find_packages(),
        install_requires=['youtube-dl'],

        entry_points={'console_scripts': ['chain-dl = chain_dl:main']}
)
