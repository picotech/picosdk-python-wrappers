#
# Copyright (C) 2018-2022 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 BLOCK MODE ADVANCED TRIGGER EXAMPLE
# This example opens a 6000 driver device, sets up one channel and a window pulse width advanced trigger then collects a block of data.
# This data is then plotted as mV against time in ns.

import ctypes
import numpy as np
from picosdk.ps6000 import ps6000 as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok, mV2adc

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 6000 series PicoScope
# Returns handle to chandle for use in future API functions
status["openunit"] = ps.ps6000OpenUnit(ctypes.byref(chandle), None)
assert_pico_ok(status["openunit"])

# Set up channel A
# handle = chandle
# channel = PS6000_CHANNEL_A = 0
# enabled = 1
# coupling type = PS6000_DC = 1
# range = PS6000_2V = 7
# analogue offset = 0 V
# bandwidth limiter = PS6000_BW_FULL = 0
chARange = 7
status["setChA"] = ps.ps6000SetChannel(chandle, 0, 1, 1, chARange, 0, 0)
assert_pico_ok(status["setChA"])

# Set up window pulse width trigger on A
triggerConditions = ps.PS6000_TRIGGER_CONDITIONS(ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_TRUE"],
												ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"],
												ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"],
												ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"],
												ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"],
												ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"],
												ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_TRUE"])
nTriggerConditions = 1

status["setTriggerChannelConditions"] = ps.ps6000SetTriggerChannelConditions(chandle, ctypes.byref(triggerConditions), nTriggerConditions)
assert_pico_ok(status["setTriggerChannelConditions"])

status["setTriggerChannelDirections"] = ps.ps6000SetTriggerChannelDirections(chandle, 
																			ps.PS6000_THRESHOLD_DIRECTION["PS6000_INSIDE"], 
																			ps.PS6000_THRESHOLD_DIRECTION["PS6000_NONE"],
																			ps.PS6000_THRESHOLD_DIRECTION["PS6000_NONE"], 
																			ps.PS6000_THRESHOLD_DIRECTION["PS6000_NONE"], 
																			ps.PS6000_THRESHOLD_DIRECTION["PS6000_NONE"],
																			ps.PS6000_THRESHOLD_DIRECTION["PS6000_NONE"])
assert_pico_ok(status["setTriggerChannelDirections"])

maxADC = ctypes.c_int16(32512)
threshold = mV2adc(109.2, chARange, maxADC)
hysteresis = mV2adc((109.2 * 0.015), chARange, maxADC)
channelProperties = ps.PS6000_TRIGGER_CHANNEL_PROPERTIES(threshold,
														hysteresis,
														(threshold * -1),
														hysteresis,
														ps.PS6000_CHANNEL["PS6000_CHANNEL_A"],
														ps.PS6000_THRESHOLD_MODE["PS6000_WINDOW"])
nChannelProperties = 1
auxOutputEnable = 0
autoTriggerMilliseconds = 10000
status["setTriggerChannelProperties"] = ps.ps6000SetTriggerChannelProperties(chandle, ctypes.byref(channelProperties), nChannelProperties, auxOutputEnable, autoTriggerMilliseconds)
assert_pico_ok(status["setTriggerChannelProperties"])

pwqConditions = ps.PS6000_PWQ_CONDITIONS(ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_TRUE"],
										ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"],
										ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"],
										ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"],
										ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"],
										ps.PS6000_TRIGGER_STATE["PS6000_CONDITION_DONT_CARE"])
nPwqConditions = 1
direction = ps.PS6000_THRESHOLD_DIRECTION["PS6000_RISING_OR_FALLING"]
upper = 390625 #samples at timebase 8 is 10 ms
lower = upper
type = ps.PS6000_PULSE_WIDTH_TYPE["PS6000_PW_TYPE_GREATER_THAN"]
status["setPulseWidthQualifier"] = ps.ps6000SetPulseWidthQualifier(chandle, ctypes.byref(pwqConditions), nPwqConditions, direction, lower, upper, type)
assert_pico_ok(status["setPulseWidthQualifier"])

# Set number of pre and post trigger samples to be collected
preTriggerSamples = 390625*2
postTriggerSamples = 390625
maxSamples = preTriggerSamples + postTriggerSamples

# Get timebase information
# Warning: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
# To access these Timebases, set any unused analogue channels to off.
# handle = chandle
# timebase = 8 = timebase
# noSamples = maxSamples
# pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalns)
# oversample = 1
# pointer to maxSamples = ctypes.byref(returnedMaxSamples)
# segment index = 0
timebase = 8
timeIntervalns = ctypes.c_float()
returnedMaxSamples = ctypes.c_int32()
status["getTimebase2"] = ps.ps6000GetTimebase2(chandle, timebase, maxSamples, ctypes.byref(timeIntervalns), 1, ctypes.byref(returnedMaxSamples), 0)
assert_pico_ok(status["getTimebase2"])

# Run block capture
# handle = chandle
# number of pre-trigger samples = preTriggerSamples
# number of post-trigger samples = PostTriggerSamples
# timebase = 8 = 80 ns (see Programmer's guide for mre information on timebases)
# oversample = 0
# time indisposed ms = None (not needed in the example)
# segment index = 0
# lpReady = None (using ps6000IsReady rather than ps6000BlockReady)
# pParameter = None
status["runBlock"] = ps.ps6000RunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, 0, None, 0, None, None)
assert_pico_ok(status["runBlock"])

# Check for data collection to finish using ps6000IsReady
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.ps6000IsReady(chandle, ctypes.byref(ready))

# Create buffers ready for assigning pointers for data collection
bufferAMax = (ctypes.c_int16 * maxSamples)()
bufferAMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example
bufferBMax = (ctypes.c_int16 * maxSamples)()
bufferBMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example

# Set data buffer location for data collection from channel A
# handle = chandle
# source = PS6000_CHANNEL_A = 0
# pointer to buffer max = ctypes.byref(bufferAMax)
# pointer to buffer min = ctypes.byref(bufferAMin)
# buffer length = maxSamples
# ratio mode = PS6000_RATIO_MODE_NONE = 0
status["setDataBuffersA"] = ps.ps6000SetDataBuffers(chandle, 0, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxSamples, 0)
assert_pico_ok(status["setDataBuffersA"])

# create overflow loaction
overflow = ctypes.c_int16()
# create converted type maxSamples
cmaxSamples = ctypes.c_int32(maxSamples)

# Retried data from scope to buffers assigned above
# handle = chandle
# start index = 0
# pointer to number of samples = ctypes.byref(cmaxSamples)
# downsample ratio = 1
# downsample ratio mode = PS6000_RATIO_MODE_NONE
# pointer to overflow = ctypes.byref(overflow))
status["getValues"] = ps.ps6000GetValues(chandle, 0, ctypes.byref(cmaxSamples), 1, 0, 0, ctypes.byref(overflow))
assert_pico_ok(status["getValues"])

# find maximum ADC count value
maxADC = ctypes.c_int16(32512)

# convert ADC counts data to mV
adc2mVChAMax =  adc2mV(bufferAMax, chARange, maxADC)

# Create time data
time = np.linspace(0, (cmaxSamples.value -1) * timeIntervalns.value, cmaxSamples.value)

# plot data from channel A
plt.plot(time, adc2mVChAMax[:])
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (mV)')
plt.show()

status["stop"] = ps.ps6000Stop(chandle)
assert_pico_ok(status["stop"])

# Close unitDisconnect the scope
# handle = chandle
ps.ps6000CloseUnit(chandle)

# display status returns
print(status)