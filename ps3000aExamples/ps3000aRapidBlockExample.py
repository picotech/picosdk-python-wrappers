#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PS3000A RAPID BLOCK MODE EXAMPLE
# This example opens a 3000a driver device, sets up one channel and a trigger then collects 10 block of data in rapid succession.
# This data is then plotted as mV against time in ns.

import ctypes
from picosdk.ps3000a import ps3000a as ps
import numpy as np
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok

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

# Sets up single trigger
# Handle = Chandle
# Enable = 1
# Source = ps3000A_channel_A = 0
# Threshold = 1024 ADC counts
# Direction = ps3000A_Falling = 3
# Delay = 0
# autoTrigger_ms = 1000
status["trigger"] = ps.ps3000aSetSimpleTrigger(chandle, 1, 0, 1024, 3, 0, 1000)
assert_pico_ok(status["trigger"])

# Setting the number of sample to be collected
preTriggerSamples = 40000
postTriggerSamples = 40000
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

# Handle = Chandle
# nSegments = 10
# nMaxSamples = ctypes.byref(cmaxSamples)

status["MemorySegments"] = ps.ps3000aMemorySegments(chandle, 10, ctypes.byref(cmaxSamples))
assert_pico_ok(status["MemorySegments"])

# sets number of captures
status["SetNoOfCaptures"] = ps.ps3000aSetNoOfCaptures(chandle, 10)
assert_pico_ok(status["SetNoOfCaptures"])

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
#bufferAMax = (ctypes.c_int16 * maxsamples)()
#bufferAMin = (ctypes.c_int16 * maxsamples)() # used for downsampling which isn't in the scope of this example

bufferAMax = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin = np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 0
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax.ctypes.data, bufferAMin.ctypes.data, maxsamples, 0, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax1 = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin1 = np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax1)
# Buffer min = ctypes.byref(bufferAMin1)
# Buffer length = maxsamples
# Segment index = 1
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax1.ctypes.data, bufferAMin1.ctypes.data, maxsamples, 1, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax2 = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin2 = np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 2
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax2.ctypes.data, bufferAMin2.ctypes.data, maxsamples, 2, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax3 = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin3 =np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 3
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax3.ctypes.data, bufferAMin3.ctypes.data, maxsamples, 3, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax4 = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin4 = np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 4
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax4.ctypes.data, bufferAMin4.ctypes.data, maxsamples, 4, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax5 = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin5 = np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 5
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax5.ctypes.data, bufferAMin5.ctypes.data, maxsamples, 5, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax6 = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin6 = np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 6
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax6.ctypes.data, bufferAMin6.ctypes.data, maxsamples, 6, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax7 = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin7 = np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 7
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax7.ctypes.data, bufferAMin7.ctypes.data, maxsamples, 7, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax8 = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin8 = np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 8
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax8.ctypes.data, bufferAMin8.ctypes.data, maxsamples, 8, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax9 = np.empty(maxsamples, dtype=np.dtype('int16'))
bufferAMin9 = np.empty(maxsamples, dtype=np.dtype('int16')) # used for downsampling which isn't in the scope of this example

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps3000A_channel_A = 0
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 9
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0, bufferAMax9.ctypes.data, bufferAMin9.ctypes.data, maxsamples, 9, 0)
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
# noOfSamples = ctypes.byref(cmaxSamples)
# fromSegmentIndex = 0
# ToSegmentIndex = 9
# DownSampleRatio = 0
# DownSampleRatioMode = 0
# Overflow = ctypes.byref(overflow)

status["GetValuesBulk"] = ps.ps3000aGetValuesBulk(chandle, ctypes.byref(cmaxSamples), 0, 9, 1, 0, ctypes.byref(overflow))
assert_pico_ok(status["GetValuesBulk"])

# Handle = chandle
# Times = Times = (ctypes.c_int16*10)() = ctypes.byref(Times)
# Timeunits = TimeUnits = ctypes.c_char() = ctypes.byref(TimeUnits)
# Fromsegmentindex = 0
# Tosegementindex = 9
Times = (ctypes.c_int16*10)()
TimeUnits = ctypes.c_char()
status["GetValuesTriggerTimeOffsetBulk"] = ps.ps3000aGetValuesTriggerTimeOffsetBulk64(chandle, ctypes.byref(Times), ctypes.byref(TimeUnits), 0, 9)
assert_pico_ok(status["GetValuesTriggerTimeOffsetBulk"])

# Finds the max ADC count
# Handle = chandle
# Value = ctype.byref(maxADC)
maxADC = ctypes.c_int16()
status["maximumValue"] = ps.ps3000aMaximumValue(chandle, ctypes.byref(maxADC))
assert_pico_ok(status["maximumValue"])

# Converts ADC from channel A to mV
adc2mVChAMax =  adc2mV(bufferAMax, chARange, maxADC)
adc2mVChAMax1 =  adc2mV(bufferAMax1, chARange, maxADC)
adc2mVChAMax2 =  adc2mV(bufferAMax2, chARange, maxADC)
adc2mVChAMax3 =  adc2mV(bufferAMax3, chARange, maxADC)
adc2mVChAMax4 =  adc2mV(bufferAMax4, chARange, maxADC)
adc2mVChAMax5 =  adc2mV(bufferAMax5, chARange, maxADC)
adc2mVChAMax6 =  adc2mV(bufferAMax6, chARange, maxADC)
adc2mVChAMax7 =  adc2mV(bufferAMax7, chARange, maxADC)
adc2mVChAMax8 =  adc2mV(bufferAMax8, chARange, maxADC)
adc2mVChAMax9 =  adc2mV(bufferAMax9, chARange, maxADC)

# Creates the time data
time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)

# Plots the data from channel A onto a graph
plt.plot(time, adc2mVChAMax[:])
plt.plot(time, adc2mVChAMax1[:])
plt.plot(time, adc2mVChAMax2[:])
plt.plot(time, adc2mVChAMax3[:])
plt.plot(time, adc2mVChAMax4[:])
plt.plot(time, adc2mVChAMax5[:])
plt.plot(time, adc2mVChAMax6[:])
plt.plot(time, adc2mVChAMax7[:])
plt.plot(time, adc2mVChAMax8[:])
plt.plot(time, adc2mVChAMax9[:])
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

