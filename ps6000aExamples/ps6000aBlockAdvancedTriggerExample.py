#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 A BLOCK MODE EXAMPLE
# This example opens a 6000a driver device, sets up two channels and a trigger then collects a block of data.
# This data is then plotted as mV against time in ns.

import ctypes
import numpy as np
from picosdk.ps6000a import ps6000a as ps
from picosdk.PicoDeviceEnums import picoEnum as enums
from picosdk.PicoDeviceStructs import picoStruct as struct
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok, mV2adc

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 6000 A series PicoScope
# returns handle to chandle for use in future API functions
resolution = enums.PICO_DEVICE_RESOLUTION["PICO_DR_8BIT"]
status["openunit"] = ps.ps6000aOpenUnit(ctypes.byref(chandle), None, resolution)
assert_pico_ok(status["openunit"])

# Set channel A on
# handle = chandle
channelA = enums.PICO_CHANNEL["PICO_CHANNEL_A"]
coupling = enums.PICO_COUPLING["PICO_DC"]
channelRange = 7
# analogueOffset = 0 V
bandwidth = enums.PICO_BANDWIDTH_LIMITER["PICO_BW_FULL"]
status["setChannelA"] = ps.ps6000aSetChannelOn(chandle, channelA, coupling, channelRange, 0, bandwidth)
assert_pico_ok(status["setChannelA"])

channelB = enums.PICO_CHANNEL["PICO_CHANNEL_B"]
status["setChannelB"] = ps.ps6000aSetChannelOn(chandle, channelB, coupling, channelRange, 0, bandwidth)
assert_pico_ok(status["setChannelB"])

# set channel C-H off
for x in range (2, 7, 1):
    channel = x
    status["setChannel",x] = ps.ps6000aSetChannelOff(chandle,channel)
    assert_pico_ok(status["setChannel",x])
    
# get max ADC value
# handle = chandle
minADC = ctypes.c_int16()
maxADC = ctypes.c_int16()
status["getAdcLimits"] = ps.ps6000aGetAdcLimits(chandle, resolution, ctypes.byref(minADC), ctypes.byref(maxADC))
assert_pico_ok(status["getAdcLimits"])

# use the trigger functions seperately
# set up a simple edge trigger on channel A OR B with a 1 V threshold

conditions = (struct.PICO_CONDITION * 2)()
conditions[0] = struct.PICO_CONDITION(channelA,enums.PICO_TRIGGER_STATE["PICO_CONDITION_TRUE"])
conditions[1] = struct.PICO_CONDITION(channelB, enums.PICO_TRIGGER_STATE["PICO_CONDITION_TRUE"])
nConditions = 2
clear = enums.PICO_ACTION["PICO_CLEAR_ALL"]
add = enums.PICO_ACTION["PICO_ADD"]
action = clear|add # PICO_ACTION["PICO_CLEAR_WAVEFORM_CLEAR_ALL"] | PICO_ACTION["PICO_ADD"]  
status["setTriggerChannelConditions"] = ps.ps6000aSetTriggerChannelConditions(chandle, ctypes.byref(conditions), nConditions, action)
assert_pico_ok(status["setTriggerChannelConditions"])

directions = (struct.PICO_DIRECTION * 2)()
directions[0]= struct.PICO_DIRECTION(channelA, enums.PICO_THRESHOLD_DIRECTION["PICO_RISING"], enums.PICO_THRESHOLD_MODE["PICO_LEVEL"])
directions[1]= struct.PICO_DIRECTION(channelB, enums.PICO_THRESHOLD_DIRECTION["PICO_RISING"], enums.PICO_THRESHOLD_MODE["PICO_LEVEL"])
nDirections = 2
status["setTriggerChannelDirections"] = ps.ps6000aSetTriggerChannelDirections(chandle,ctypes.byref(directions),nDirections)
assert_pico_ok(status["setTriggerChannelDirections"])

channelProperties = (struct.PICO_TRIGGER_CHANNEL_PROPERTIES * 2)()
channelProperties[0] = struct.PICO_TRIGGER_CHANNEL_PROPERTIES(mV2adc(1000,channelRange,maxADC), 0, 0, 0, channelA)
channelProperties[1] = struct.PICO_TRIGGER_CHANNEL_PROPERTIES(mV2adc(1000,channelRange,maxADC), 0, 0, 0, channelB)
nChannelProperties = 2
autoTriggerMicroSeconds = 1000000
status["setTriggerChannelProperties"] = ps.ps6000aSetTriggerChannelProperties(chandle, ctypes.byref(channelProperties),nChannelProperties,0,autoTriggerMicroSeconds)
assert_pico_ok(status["setTriggerChannelProperties"])

# Get fastest available timebase
# handle = chandle
enabledChannelFlags = enums.PICO_CHANNEL_FLAGS["PICO_CHANNEL_A_FLAGS"] + enums.PICO_CHANNEL_FLAGS["PICO_CHANNEL_B_FLAGS"]
timebase = ctypes.c_uint32(0)
timeInterval = ctypes.c_double(0)
# resolution = resolution
status["getMinimumTimebaseStateless"] = ps.ps6000aGetMinimumTimebaseStateless(chandle, enabledChannelFlags, ctypes.byref(timebase), ctypes.byref(timeInterval), resolution)
print("timebase = ", timebase.value)
print("sample interval =", timeInterval.value, "s")

# Set number of samples to be collected
noOfPreTriggerSamples = 500000
noOfPostTriggerSamples = 1000000
nSamples = noOfPostTriggerSamples + noOfPreTriggerSamples

# Create buffers
bufferAMax = (ctypes.c_int16 * nSamples)()
bufferAMin = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferBMax = (ctypes.c_int16 * nSamples)()
bufferBMin = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example

# Set data buffers
# handle = chandle
# channel = channelA
# bufferMax = bufferAMax
# bufferMin = bufferAMin
# nSamples = nSamples
dataType = enums.PICO_DATA_TYPE["PICO_INT16_T"]
waveform = 0
downSampleMode = enums.PICO_RATIO_MODE["PICO_RATIO_MODE_RAW"]
action = clear|add # PICO_ACTION["PICO_CLEAR_WAVEFORM_CLEAR_ALL"] | PICO_ACTION["PICO_ADD"]  
status["setDataBuffers"] = ps.ps6000aSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), nSamples, dataType, waveform, downSampleMode, action)
assert_pico_ok(status["setDataBuffers"])
status["setDataBuffers"] = ps.ps6000aSetDataBuffers(chandle, channelB, ctypes.byref(bufferBMax), ctypes.byref(bufferBMin), nSamples, dataType, waveform, downSampleMode, action)
assert_pico_ok(status["setDataBuffers"])

# Run block capture
# handle = chandle
# timebase = timebase
timeIndisposedMs = ctypes.c_double(0)
# segmentIndex = 0
# lpReady = None   Using IsReady rather than a callback
# pParameter = None
status["runBlock"] = ps.ps6000aRunBlock(chandle, noOfPreTriggerSamples, noOfPostTriggerSamples, timebase, ctypes.byref(timeIndisposedMs), 0, None, None)
assert_pico_ok(status["runBlock"])

# Check for data collection to finish using ps6000aIsReady
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.ps6000aIsReady(chandle, ctypes.byref(ready))
    
# Get data from scope
# handle = chandle
# startIndex = 0
noOfSamples = ctypes.c_uint64(nSamples)
# downSampleRatio = 1
# segmentIndex = 0
overflow = ctypes.c_int16(0)
status["getValues"] = ps.ps6000aGetValues(chandle, 0, ctypes.byref(noOfSamples), 1, downSampleMode, 0, ctypes.byref(overflow))
assert_pico_ok(status["getValues"])

# convert ADC counts data to mV
adc2mVChAMax =  adc2mV(bufferAMax, channelRange, maxADC)
adc2mVChBMax =  adc2mV(bufferBMax, channelRange, maxADC)

# Create time data
time = np.linspace(0, (nSamples -1) * timeInterval.value * 1000000000, nSamples)

# plot data from channel A and B
plt.plot(time, adc2mVChAMax[:])
plt.plot(time, adc2mVChBMax[:])
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (mV)')
plt.show()

# Close the scope
status["closeunit"] = ps.ps6000aCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

print(status)