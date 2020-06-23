#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 GET INFO EXAMPLE
# This example opens a 6000 driver device, gets the variant info and closes the scope.

import ctypes
import numpy as np
from picosdk.ps6000 import ps6000 as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 6000 series PicoScope
# Returns handle to chandle for use in future API functions
status["openunit"] = ps.ps6000OpenUnit(ctypes.byref(chandle), None)
assert_pico_ok(status["openunit"])

# Get Info from scope
string = ctypes.c_int8()
stringLength = ctypes.c_int16(1)
requiredSize = ctypes.c_int16()
info = ps.PICO_INFO["PICO_VARIANT_INFO"]
status["getInfo"] = ps.ps6000GetUnitInfo(chandle, ctypes.byref(string),stringLength, ctypes.byref(requiredSize), info)
assert_pico_ok(status["getInfo"])

# Close unitDisconnect the scope
# handle = chandle
ps.ps6000CloseUnit(chandle)

# display status returns
print(status)