#
# Copyright (C) 2017-2018 Pico Technology Ltd.
#
from __future__ import print_function
from setuptools import setup

import ctypes
from ctypes import *
from ctypes.util import find_library
import sys
import os.path


signalfile = ".sdkwarning"
if not os.path.exists(signalfile):
    name = 'ps2000'
    try:
        if sys.platform == 'win32':
            result = ctypes.WinDLL(find_library(name))
        else:
            result = cdll.LoadLibrary(find_library(name))
    except OSError:
        print("Please install the PicoSDK in order to use this wrapper."
              "Visit https://www.picotech.com/downloads")
        exit(1)
    open(signalfile, 'a').close()

with open("README.md") as f:
    readme = f.read()

setup(
    name='picosdk',
    packages=['picosdk'],
    install_requires=["numpy>=1.12.1"],
    version='1.0',
    description='PicoSDK Python wrapper',
    long_description=readme,
    author='Pico Technology Ltd',
    author_email='support@picotech.com',
    license="ISC",
    url='https://www.picotech.com',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Framework :: Matplotlib",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ],
    universal=True,
)
