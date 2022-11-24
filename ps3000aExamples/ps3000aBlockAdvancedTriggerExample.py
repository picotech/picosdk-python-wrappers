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
from picosdk.functions import adc2mV, mV2adc, assert_pico_ok

# Create chandle and status ready for use
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps3000aOpenUnit(ctypes.byref(chandle), None)

try:
    assert_pico_ok(status["openunit"])
except:

    # powerstate becomes the status number of openunit
    powerstate = status["openunit"]

    # If powerstate is the same as 282 then it will run this if statement
    if powerstate == 282:
        # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
        status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 282)
        # If the powerstate is the same as 286 then it will run this if statement
    elif powerstate == 286:
        # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
        status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 286)
    else:
        raise

    assert_pico_ok(status["ChangePowerSource"])

# Set up channel A
# handle = chandle
# channel = PS3000A_CHANNEL_A = 0
# enabled = 1
# coupling type = PS3000A_DC = 1
# range = PS3000A_10V = 8
# analogue offset = 0 V
chARange = 8
status["setChA"] = ps.ps3000aSetChannel(chandle, 0, 1, 1, chARange, 0)
assert_pico_ok(status["setChA"])

# Finds the max ADC count
# Handle = chandle
# Value = ctypes.byref(maxADC)
maxADC = ctypes.c_int16()
status["maximumValue"] = ps.ps3000aMaximumValue(chandle, ctypes.byref(maxADC))
assert_pico_ok(status["maximumValue"])

# Set an advanced trigger
adcTriggerLevel = mV2adc(500, chARange, maxADC)

# set trigger channel properties
# handle = chandle
channelProperties = ps.PS3000A_TRIGGER_CHANNEL_PROPERTIES(adcTriggerLevel,
                                                          10,
                                                          adcTriggerLevel,
                                                          10,
                                                          ps.PS3000A_CHANNEL["PS3000A_CHANNEL_A"],
                                                          ps.PS3000A_THRESHOLD_MODE["PS3000A_LEVEL"])
nChannelProperties = 1
# auxOutputEnabled = 0
autoTriggerMilliseconds = 10000
status["setTrigProp"] = ps.ps3000aSetTriggerChannelProperties(chandle, ctypes.byref(channelProperties), nChannelProperties, 0, autoTriggerMilliseconds)
assert_pico_ok(status["setTrigProp"])

# set trigger conditions V2
# chandle = handle
conditions = ps.PS3000A_TRIGGER_CONDITIONS_V2(ps.PS3000A_TRIGGER_STATE["PS3000A_CONDITION_TRUE"],
                                              ps.PS3000A_TRIGGER_STATE["PS3000A_CONDITION_DONT_CARE"],
                                              ps.PS3000A_TRIGGER_STATE["PS3000A_CONDITION_DONT_CARE"],
                                              ps.PS3000A_TRIGGER_STATE["PS3000A_CONDITION_DONT_CARE"],
                                              ps.PS3000A_TRIGGER_STATE["PS3000A_CONDITION_DONT_CARE"],
                                              ps.PS3000A_TRIGGER_STATE["PS3000A_CONDITION_DONT_CARE"],
                                              ps.PS3000A_TRIGGER_STATE["PS3000A_CONDITION_DONT_CARE"],
                                              ps.PS3000A_TRIGGER_STATE["PS3000A_CONDITION_DONT_CARE"])
nConditions = 1
status["setTrigCond"] = ps.ps3000aSetTriggerChannelConditionsV2(chandle, ctypes.byref(conditions), nConditions)
assert_pico_ok(status["setTrigCond"])

# set trigger directions
# handle = chandle
channelADirection = ps.PS3000A_THRESHOLD_DIRECTION["PS3000A_RISING"]
channelBDirection = ps.PS3000A_THRESHOLD_DIRECTION["PS3000A_NONE"]
channelCDirection = ps.PS3000A_THRESHOLD_DIRECTION["PS3000A_NONE"]
channelDDirection = ps.PS3000A_THRESHOLD_DIRECTION["PS3000A_NONE"]
extDirection = ps.PS3000A_THRESHOLD_DIRECTION["PS3000A_NONE"]
auxDirection = ps.PS3000A_THRESHOLD_DIRECTION["PS3000A_NONE"]
status["setTrigDir"] = ps.ps3000aSetTriggerChannelDirections(chandle, channelADirection, channelBDirection, channelCDirection, channelDDirection, extDirection, auxDirection)
assert_pico_ok(status["setTrigDir"])

# Setting the number of sample to be collected
preTriggerSamples = 00000
postTriggerSamples = 50000
maxsamples = preTriggerSamples + postTriggerSamples

# Gets timebase innfomation
# WARNING: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
# To access these Timebases, set any unused analogue channels to off.
# Handle = chandle
# Timebase = 2 = timebase
# Nosample = maxsamples
# TimeIntervalNanoseconds = ctypes.byref(timeIntervalns)
# MaxSamples = ctypes.byref(returnedMaxSamples)
# Segement index = 0
timebase = 2
timeIntervalns = ctypes.c_float()
returnedMaxSamples = ctypes.c_int16()
status["GetTimebase"] = ps.ps3000aGetTimebase2(chandle, timebase, maxsamples, ctypes.byref(timeIntervalns), 1, ctypes.byref(returnedMaxSamples), 0)
assert_pico_ok(status["GetTimebase"])

# Creates a overlow location for data
overflow = ctypes.c_int16()
# Creates converted types maxsamples
cmaxSamples = ctypes.c_int32(maxsamples)

# Starts the block capture
# Handle = chandle
# Number of prTriggerSamples
# Number of postTriggerSamples
# Timebase = 2 = 4ns (see Programmer's guide for more information on timebases)
# time indisposed ms = None (This is not needed within the example)
# Segment index = 0
# LpRead = None
# pParameter = None
status["runblock"] = ps.ps3000aRunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, 1, None, 0, None, None)
assert_pico_ok(status["runblock"])

# Create buffers ready for assigning pointers for data collection
bufferAMax = (ctypes.c_int16 * maxsamples)()
bufferAMin = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 0
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxsamples, 0, 0)
assert_pico_ok(status["SetDataBuffers"])

# Creates a overlow location for data
overflow = (ctypes.c_int16 * 10)()
# Creates converted types maxsamples
cmaxSamples = ctypes.c_int32(maxsamples)

# Checks data collection to finish the capture
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.ps3000aIsReady(chandle, ctypes.byref(ready))

# Handle = chandle
# start index = 0
# noOfSamples = ctypes.byref(cmaxSamples)
# DownSampleRatio = 0
# DownSampleRatioMode = 0
# SegmentIndex = 0
# Overflow = ctypes.byref(overflow)

status["GetValues"] = ps.ps3000aGetValues(chandle, 0, ctypes.byref(cmaxSamples), 0, 0, 0, ctypes.byref(overflow))
assert_pico_ok(status["GetValues"])

# Converts ADC from channel A to mV
adc2mVChAMax =  adc2mV(bufferAMax, chARange, maxADC)

# Creates the time data
time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)

# Plots the data from channel A onto a graph
plt.plot(time, adc2mVChAMax[:])
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (mV)')
plt.show()

# Stops the scope
# Handle = chandle
status["stop"] = ps.ps3000aStop(chandle)
assert_pico_ok(status["stop"])

# Closes the unit
# Handle = chandle
status["close"] = ps.ps3000aCloseUnit(chandle)
assert_pico_ok(status["close"])

# Displays the staus returns
print(status)

