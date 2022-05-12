#
# Copyright (C) 2018-2022 Pico Technology Ltd. See LICENSE file for terms.
#
# ps5000 RAPID BLOCK MODE EXAMPLE
# This example opens a 5000 driver device, sets up one channel and a trigger then collects 10 block of data in rapid succession.
# This data is then plotted as mV against time in ns.

import ctypes
from picosdk.ps5000 import ps5000 as ps
import numpy as np
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok, mV2adc

# Create chandle and status ready for use
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps5000OpenUnit(ctypes.byref(chandle))
assert_pico_ok(status["openunit"])


# Displays the serial number and handle
print(chandle.value)

# Set up channel A
# handle = chandle
channel = ps.PS5000_CHANNEL["PS5000_CHANNEL_A"]
# enabled = 1
coupling_type = 1 # DC
chARange = ps.PS5000_RANGE["PS5000_5V"]
status["setChA"] = ps.ps5000SetChannel(chandle, channel, 1, coupling_type, chARange, 0)
assert_pico_ok(status["setChA"])


# Finds the max ADC count
# Handle = chandle
# Value = ctype.byref(maxADC)
maxADC = ctypes.c_int16(32512)


# Set up single trigger
# handle = chandle
# enabled = 1
source = ps.PS5000_CHANNEL["PS5000_CHANNEL_A"]
threshold = int(mV2adc(500,chARange, maxADC))
# direction = PS5000_RISING = 2
# delay = 0 s
# auto Trigger = 1000 ms
status["trigger"] = ps.ps5000SetSimpleTrigger(chandle, 1, source, threshold, 2, 0, 1000)
assert_pico_ok(status["trigger"])

# Setting the number of sample to be collected
preTriggerSamples = 400
postTriggerSamples = 400
maxsamples = preTriggerSamples + postTriggerSamples

# Gets timebase innfomation
# Warning: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
# To access these Timebases, set any unused analogue channels to off.
# Handle = chandle
timebase = 2
# Nosample = maxsamples
# TimeIntervalNanoseconds = ctypes.byref(timeIntervalns)
# MaxSamples = ctypes.byref(returnedMaxSamples)
# Segement index = 0
timeIntervalns = ctypes.c_float()
oversample = 1
returnedMaxSamples = ctypes.c_int16()
status["GetTimebase"] = ps.ps5000GetTimebase(chandle, timebase, maxsamples, ctypes.byref(timeIntervalns), oversample, ctypes.byref(returnedMaxSamples), 0)
assert_pico_ok(status["GetTimebase"])

# Creates a overlow location for data
overflow = ctypes.c_int16()
# Creates converted types maxsamples
cmaxSamples = ctypes.c_int32(maxsamples)

# Handle = Chandle
# nSegments = 10
# nMaxSamples = ctypes.byref(cmaxSamples)
status["MemorySegments"] = ps.ps5000MemorySegments(chandle, 10, ctypes.byref(cmaxSamples))
assert_pico_ok(status["MemorySegments"])

# sets number of captures
status["SetNoOfCaptures"] = ps.ps5000SetNoOfCaptures(chandle, 10)
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
status["runblock"] = ps.ps5000RunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, oversample, None, 0, None, None)
assert_pico_ok(status["runblock"])

# Create buffers ready for assigning pointers for data collection
bufferAMax = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
source = ps.PS5000_CHANNEL["PS5000_CHANNEL_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 0
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxsamples, 0)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax1 = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps.PS5000_CHANNEL["ps5000_channel_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 1
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax1), ctypes.byref(bufferAMin1), maxsamples, 1)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax2 = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps.PS5000_CHANNEL["ps5000_channel_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 2
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax2), ctypes.byref(bufferAMin2), maxsamples, 2)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax3 = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps.PS5000_CHANNEL["ps5000_channel_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 3
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax3), ctypes.byref(bufferAMin3), maxsamples, 3)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax4 = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps.PS5000_CHANNEL["ps5000_channel_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 4
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax4), ctypes.byref(bufferAMin4), maxsamples, 4)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax5 = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps.PS5000_CHANNEL["ps5000_channel_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 5
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax5), ctypes.byref(bufferAMin5), maxsamples, 5)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax6 = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps.PS5000_CHANNEL["ps5000_channel_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 6
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax6), ctypes.byref(bufferAMin6), maxsamples, 6)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax7 = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps.PS5000_CHANNEL["ps5000_channel_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 7
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax7), ctypes.byref(bufferAMin7), maxsamples, 7)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax8 = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps.PS5000_CHANNEL["ps5000_channel_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 8
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax8), ctypes.byref(bufferAMin8), maxsamples, 8)
assert_pico_ok(status["SetDataBuffers"])

# Create buffers ready for assigning pointers for data collection
bufferAMax9 = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from channel A
# Handle = Chandle
# source = ps.PS5000_CHANNEL["ps5000_channel_A"]
# Buffer max = ctypes.byref(bufferAMax)
# Buffer length = maxsamples
# Segment index = 9
status["SetDataBuffers"] = ps.ps5000SetDataBufferBulk(chandle, source, ctypes.byref(bufferAMax9), ctypes.byref(bufferAMin9), maxsamples, 9)
assert_pico_ok(status["SetDataBuffers"])

# Creates a overlow location for data
overflow = (ctypes.c_int16 * 10)()
# Creates converted types maxsamples
cmaxSamples = ctypes.c_int32(maxsamples)

# Checks data collection to finish the capture
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.ps5000IsReady(chandle, ctypes.byref(ready))

# Handle = chandle
# noOfSamples = ctypes.byref(cmaxSamples)
# fromSegmentIndex = 0
# ToSegmentIndex = 9
# DownSampleRatio = 0
# DownSampleRatioMode = 0
# Overflow = ctypes.byref(overflow)

status["GetValuesBulk"] = ps.ps5000GetValuesBulk(chandle, ctypes.byref(cmaxSamples), 0, 9, ctypes.byref(overflow))
assert_pico_ok(status["GetValuesBulk"])

# Handle = chandle
# Times = Times = (ctypes.c_int16*10)() = ctypes.byref(Times)
# Timeunits = TimeUnits = ctypes.c_char() = ctypes.byref(TimeUnits)
# Fromsegmentindex = 0
# Tosegementindex = 9
Times = (ctypes.c_int16*10)()
TimeUnits = ctypes.c_char()
status["GetValuesTriggerTimeOffsetBulk"] = ps.ps5000GetValuesTriggerTimeOffsetBulk64(chandle, ctypes.byref(Times), ctypes.byref(TimeUnits), 0, 9)
assert_pico_ok(status["GetValuesTriggerTimeOffsetBulk"])

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
status["stop"] = ps.ps5000Stop(chandle)
assert_pico_ok(status["stop"])

# Closes the unit
# Handle = chandle
status["close"] = ps.ps5000CloseUnit(chandle)
assert_pico_ok(status["close"])

# Displays the staus returns
#print(status)


