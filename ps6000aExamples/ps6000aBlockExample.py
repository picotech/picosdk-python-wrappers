#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 A BLOCK MODE EXAMPLE
# This example opens a 6000a driver device, sets up two channels and a trigger then collects a block of data.
# This data is then plotted as mV against time in ns.

import ctypes
import numpy as np
from picosdk.ps6000a import ps6000a as ps
#from picosdk.PicoDeviceEnums import PicoDeviceEnums as enums
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 6000 A series PicoScope
# returns handle to chandle for use in future API functions
status["openunit"] = ps.ps6000aOpenUnit(ctypes.byref(chandle), None, 0)
assert_pico_ok(status["openunit"])

# Set channel A on
# handle = chandle
channel = 0 #enums.PICO_CHANNEL["PICO_CHANNEL_A"]
coupling = 0 #enums.PICO_COUPLING["PICO_DC"]
range = 7
# analogueOffset = 0 V
bandwidth = 0 #enums.PICO_CHANNEL["PICO_BW_FULL"]
status["setChannelA"] = ps.ps6000aSetChannelOn(chandle, channel, coupling, range, 0, bandwidth)
assert_pico_ok(status["setChannelA"])

# Close the scope
status["closeunit"] = ps.ps6000aCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

print(status)