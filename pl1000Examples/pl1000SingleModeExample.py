#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# PL1000 SINGLE MODE EXAMPLE
# This example opens a pl1000 device, sets up the device for capturing data from channel 1.
# Then this example collect a sample from channel 1 and displays it on the console.

import ctypes
import numpy as np
from picosdk.pl1000 import pl1000 as pl
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open PicoLog 1000 device
status["openUnit"] = pl.pl1000OpenUnit(ctypes.byref(chandle))
assert_pico_ok(status["openUnit"])

value = ctypes.c_int16()
# get a single values from channel 1
status["getSingle"] = pl.pl1000GetSingle(chandle, pl.PL1000Inputs["PL1000_CHANNEL_1"], ctypes.byref(value))
assert_pico_ok(status["getSingle"])
print(value.value)

# close PicoLog 1000 device
status["closeUnit"] = pl.pl1000CloseUnit(chandle)
assert_pico_ok(status["closeUnit"])

# display status returns
print(status)
