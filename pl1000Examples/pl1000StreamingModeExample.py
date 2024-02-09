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
from picosdk.functions import adc2mVpl1000, assert_pico_ok
from time import sleep

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open PicoLog 1000 device
status["openUnit"] = pl.pl1000OpenUnit(ctypes.byref(chandle))
assert_pico_ok(status["openUnit"])

# set sampling interval
usForBlock = ctypes.c_uint32(10000000)
noOfValues = ctypes.c_uint32(1000000)
channels = ctypes.c_int16(1)

status["setInterval"] = pl.pl1000SetInterval(chandle, ctypes.byref(usForBlock), noOfValues, ctypes.byref(channels), 1)
assert_pico_ok(status["setInterval"])

# start streaming
mode = pl.PL1000_BLOCK_METHOD["BM_STREAM"]
status["run"] = pl.pl1000Run(chandle, 1000000, mode)
assert_pico_ok(status["run"])

sleep(usForBlock.value / 1000000)

values = (ctypes.c_uint16 * noOfValues.value)()
oveflow = ctypes.c_uint16()

status["getValues"] = pl.pl1000GetValues(chandle, ctypes.byref(values), ctypes.byref(noOfValues), ctypes.byref(oveflow), None)
assert_pico_ok(status["getValues"])

# convert ADC counts data to mV
maxADC = ctypes.c_uint16()
status["maxValue"] = pl.pl1000MaxValue(chandle, ctypes.byref(maxADC))
assert_pico_ok(status["maxValue"])
inputRange = 2500
mVValues =  adc2mVpl1000(values, inputRange, maxADC)

# create time data
interval = (0.01 * usForBlock.value)/(noOfValues.value * 1)

timeMs = np.linspace(0, (len(mVValues) -1) * interval, len(mVValues))

# plot data

plt.plot(timeMs, mVValues[:])
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.show()

# close PicoLog 1000 device
status["closeUnit"] = pl.pl1000CloseUnit(chandle)
assert_pico_ok(status["closeUnit"])

# display status returns
print(status)
