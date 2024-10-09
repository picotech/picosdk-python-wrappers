#
# Copyright (C) 2024 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the enumerations from the PicoConnectProbes.h C header
file for use with various PicoScope oscilloscopes driver API functions.
"""

from ctypes import *
from picosdk.constants import make_enum
from picosdk.library import Library

class PicoConnectProbeslib(Library):
    def __init__(self):
        super(PicoConnectProbeslib, self).__init__("picoConnectProbes")


picoConnectProbes  = PicoConnectProbeslib()

def _define_pico_probe_range_info():
    PICO_PROBE_NONE_NV = 0
    PICO_X1_PROBE_NV = 1
    PICO_X10_PROBE_NV = 10
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}
    
picoConnectProbes.PICO_PROBE_RANGE_INFO = _define_pico_probe_range_info