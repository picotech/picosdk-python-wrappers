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

# Set sample interval
us_for_block = ctypes.c_int32(1000)
ideal_no_of_samples = 1000
channels = ctypes.c_int32(drDaq.USB_DRDAQ_INPUTS["USB_DRDAQ_CHANNEL_PH"])
no_of_channels = 1
status["setInterval"] = drDaq.UsbDrDaqSetInterval(chandle, ctypes.byref(us_for_block), ideal_no_of_samples, ctypes.byref(channels), no_of_channels)
assert_pico_ok(status["setInterval"])

# Find scaling information
channel = drDaq.USB_DRDAQ_INPUTS["USB_DRDAQ_CHANNEL_PH"]
nScales = ctypes.c_int16(0)
currentScale = ctypes.c_int16(0)
names = (ctypes.c_char*256)()
namesSize = 256
status["getscalings"] = drDaq.UsbDrDaqGetScalings(chandle, channel, ctypes.byref(nScales), ctypes.byref(currentScale), ctypes.byref(names), namesSize)
assert_pico_ok(status["getscalings"])

print(nScales.value)
print(currentScale.value)
print(names.value)

# Set channel scaling 
scalingNumber = 0 # pH scaling
status["setscaling"] = drDaq.UsbDrDaqSetScalings(chandle, channel, scalingNumber)
assert_pico_ok(status["setscaling"])

# Set temperature compenstation
enabled = 1
status["phTemperatureCompensation"] = drDaq.UsbDrDaqPhTemperatureCompensation(chandle, enabled)
assert_pico_ok(status["phTemperatureCompensation"])

# Run block capture
method = drDaq.USB_DRDAQ_BLOCK_METHOD["BM_SINGLE"]
status["run"] = drDaq.UsbDrDaqRun(chandle, ideal_no_of_samples, method)
assert_pico_ok(status["run"])

ready = ctypes.c_int16(0)

while ready.value == 0:
    status["ready"] = drDaq.UsbDrDaqReady(chandle, ctypes.byref(ready))
    print(ready.value)
    time.sleep(0.1)

# Retrieve data from device
values = (ctypes.c_float * ideal_no_of_samples)()
noOfValues = ctypes.c_uint32(ideal_no_of_samples)
overflow = ctypes.c_uint16(0)
triggerIndex = ctypes.c_uint32(0)
status["getvaluesF"] = drDaq.UsbDrDaqGetValuesF(chandle, ctypes.byref(values), ctypes.byref(noOfValues), ctypes.byref(overflow), ctypes.byref(triggerIndex))
assert_pico_ok(status["getvaluesF"])

# generate time data
time = np.linspace(0, us_for_block, ideal_no_of_samples)

# plot the data
plt.plot(time, values[:])
plt.xlabel('Time (ns)')
plt.ylabel('pH')
plt.show()


# Disconnect the scope
# handle = chandle
status["close"] = drDaq.UsbDrDaqCloseUnit(chandle)
assert_pico_ok(status["close"])

# Display status returns
print(status)
