# coding=utf-8
#
# Copyright (C) 2018-2019 Pico Technology Ltd. See LICENSE file for terms.
#
import ctypes
import sys

if sys.platform == 'win32':
    C_CALLBACK_FUNCTION_FACTORY = ctypes.WINFUNCTYPE
else:
    C_CALLBACK_FUNCTION_FACTORY = ctypes.CFUNCTYPE
