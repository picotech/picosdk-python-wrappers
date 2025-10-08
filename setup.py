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
atleast1dll = 0
if not os.path.exists(signalfile):
    for name in ['ps2000', 'ps3000', 'ps4000', 'ps5000', 'ps2000a', 'ps3000a', 'ps4000a', 'ps5000a', 'ps6000a', 'ps6000', 'psospa']:
        try:
            if sys.platform == 'win32':
                result = ctypes.WinDLL(find_library(name))
            else:
                result = cdll.LoadLibrary(find_library(name))
            atleast1dll = 1
        except OSError:
            print(f"Warning: PicoSDK installation is missing {name}.dll")
    if not atleast1dll:
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
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
    ],
)
