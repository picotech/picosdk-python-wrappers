#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PS3000A BLOCK MODE EXAMPLE
# This example opens a 3000a driver device, sets up one channels and a trigger then collects a block of data.
# This data is then plotted as mV against time in ns.

import ctypes
from picosdk.ps3000a import ps3000a as ps
import numpy as np
import matplotlib.pyplot as plt
from picosdk.functions import *

# Create chandle and status ready for use
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps3000aOpenUnit(ctypes.byref(chandle), None)

# powerstate becomes the status number of openunit
powerstate = status["openunit"]

# If powerstate is the same as 282 then it will run this if statement
if powerstate == 282:
    # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
    status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 282)

# If the powerstate is the same as 286 then it will run this if statement
if powerstate == 286:
    # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
    status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 286)

# Displays the serial number and handle 
print(chandle.value)

# Set up channel A
# handle = chandle
# channel = PS3000A_CHANNEL_A = 0
# enabled = 1
# coupling type = PS3000A_DC = 1
# range = PS3000A_10V = 8
# analogue offset = 0 V
chARange = 8
status["setChA"] = ps.ps3000aSetChannel(chandle, 0, 1, 1, chARange, 0)

# Sets up single trigger
# Handle = Chandle
# Enable = 0
# Source = ps3000A_channel_A = 0
# Threshold = 1024 ADC counts
# Direction = ps3000A_Falling = 3
# Delay = 0
# autoTrigger_ms = 1000
status["trigger"] = ps.ps3000aSetSimpleTrigger(chandle, 1, 0, 1024, 3, 0, 1000)

# Setting the number of sample to be collected
preTriggerSamples = 40000
postTriggerSamples = 40000
maxsamples = preTriggerSamples + postTriggerSamples

# Create buffers ready for assigning pointers for data collection
bufferAMax = (ctypes.c_int16 * maxsamples)()
bufferAMin = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 0 
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxsamples, 0, 0)

sampleInterval = ctypes.c_int32(10)
timeUnits = 3 # PS3000A_US

# Starts the streaming capture

status['runStreaming'] = ps.ps3000aRunStreaming(chandle, ctypes.byref(sampleInterval), timeUnits, preTriggerSamples, postTriggerSamples, 1, 1, 0, maxsamples)

# Stops the scope 
# Handle = chandle
status["stop"] = ps.ps3000aStop(chandle)

# Displays the staus returns
print(status)

# Closes the unit 
# Handle = chandle 
ps.ps3000aCloseUnit(chandle)

