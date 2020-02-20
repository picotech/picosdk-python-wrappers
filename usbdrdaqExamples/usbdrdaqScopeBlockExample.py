#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
# USBDRDAQ SCOPE BLOCK MODE EXAMPLE
# This example opens a UsbDrDaq driver device, sets up the scope channel and a trigger then collects a single block of data.
# This data is then plotted as mV against time in ns.

import ctypes
import time
from picosdk.usbDrDaq import usbDrDaq as drDaq
import numpy as np
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok

# Create chandle and status ready for use
status = {}
chandle = ctypes.c_int16()

# Opens the device
status["openunit"] = drDaq.UsbDrDaqOpenUnit(ctypes.byref(chandle))
assert_pico_ok(status["openunit"])

# Disconnect the scope
# handle = chandle
status["close"] = drDaq.UsbDrDaqCloseUnit(chandle)
assert_pico_ok(status["close"])

# Display status returns
print(status)
