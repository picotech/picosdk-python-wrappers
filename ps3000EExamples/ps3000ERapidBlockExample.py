#
# Copyright (C) 2024 Pico Technology Ltd. See LICENSE file for terms.
#
# PSOSPA RAPID BLOCK MODE EXAMPLE
# This example opens a psospa driver device, sets up two channels and a trigger then collects 10 blocks of data in rapid block mode.
# This data is then plotted as mV against time in ns.

import ctypes
import numpy as np
from picosdk.psospa import psospa as ps
from picosdk.PicoDeviceEnums import picoEnum as enums
from picosdk.PicoDeviceStructs import picoStruct as structs
# from picosdk.PicoConnectProbes import picoConnectProbes as probes
import matplotlib.pyplot as plt
from picosdk.functions import adc2mVV2, assert_pico_ok, mV2adcV2

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open a psospa driver device
# returns handle for future API functions
resolution = enums.PICO_DEVICE_RESOLUTION["PICO_DR_8BIT"]
status["openUnit"] = ps.psospaOpenUnit(ctypes.byref(chandle), None, resolution, None)
assert_pico_ok(status["openUnit"])

# Set channel A on
# handle = chandle
channelA = enums.PICO_CHANNEL["PICO_CHANNEL_A"]
coupling = enums.PICO_COUPLING["PICO_DC"]
rangeMax = 2000000000 #nV
rangeMin = -rangeMax #nV
rangeType = 0 #probes.PICO_PROBE_RANGE_INFO["PICO_PROBE_NONE_NV"]
analogueOffset = 0
bandwidth = enums.PICO_BANDWIDTH_LIMITER["PICO_BW_FULL"]
status["setChannelA"] = ps.psospaSetChannelOn(chandle, channelA, coupling, rangeMin, rangeMax, rangeType, analogueOffset, bandwidth)
assert_pico_ok(status["setChannelA"])

for x in range (1, 3, 1):
    channel = x
    status["setChannel",x] = ps.psospaSetChannelOff(chandle,channel)
    assert_pico_ok(status["setChannel",x])

# get max ADC value
# handle = chandle
minADC = ctypes.c_int16()
maxADC = ctypes.c_int16()
status["getAdcLimits"] = ps.psospaGetAdcLimits(chandle, resolution, ctypes.byref(minADC), ctypes.byref(maxADC))
assert_pico_ok(status["getAdcLimits"])

# Set simple trigger on channel A, 1 V rising with 1 s autotrigger
# handle = chandle
# enable = 1
source = channelA
# threshold = 100 mV
direction = enums.PICO_THRESHOLD_DIRECTION["PICO_RISING"]
# delay = 0 s
# autoTriggerMicroSeconds = 1000000 us
status["setSimpleTrigger"] = ps.psospaSetSimpleTrigger(chandle, 1, source, mV2adcV2(100,rangeMax,maxADC), direction, 0, 1000000)
assert_pico_ok(status["setSimpleTrigger"])

# Get fastest available timebase
# handle = chandle
enabledChannelFlags = enums.PICO_CHANNEL_FLAGS["PICO_CHANNEL_A_FLAGS"]
timebase = ctypes.c_uint32(0)
timeInterval = ctypes.c_double(0)
# resolution = resolution
status["getMinimumTimebaseStateless"] = ps.psospaGetMinimumTimebaseStateless(chandle, enabledChannelFlags, ctypes.byref(timebase), ctypes.byref(timeInterval), resolution)
print("timebase = ", timebase.value)
print("sample interval =", timeInterval.value, "s")

# Set number of samples to be collected
noOfPreTriggerSamples = 500000
noOfPostTriggerSamples = 1000000
nSamples = (noOfPostTriggerSamples + noOfPreTriggerSamples)

# Set number of memory segments
noOfCaptures = 20
maxSegments = ctypes.c_uint64(10)
status["memorySegments"] = ps.psospaMemorySegments(chandle, noOfCaptures, ctypes.byref(maxSegments))
assert_pico_ok(status["memorySegments"])

# Set number of captures
status["setNoOfCaptures"] = ps.psospaSetNoOfCaptures(chandle, noOfCaptures)
assert_pico_ok(status["setNoOfCaptures"])

# Create buffers
bufferAMax = (ctypes.c_int16 * nSamples)()
bufferAMin = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferAMax1 = (ctypes.c_int16 * nSamples)()
bufferAMin1 = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferAMax2 = (ctypes.c_int16 * nSamples)()
bufferAMin2 = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferAMax3 = (ctypes.c_int16 * nSamples)()
bufferAMin3 = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferAMax4 = (ctypes.c_int16 * nSamples)()
bufferAMin4 = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferAMax5 = (ctypes.c_int16 * nSamples)()
bufferAMin5 = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferAMax6 = (ctypes.c_int16 * nSamples)()
bufferAMin6 = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferAMax7 = (ctypes.c_int16 * nSamples)()
bufferAMin7 = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferAMax8 = (ctypes.c_int16 * nSamples)()
bufferAMin8 = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example
bufferAMax9 = (ctypes.c_int16 * nSamples)()
bufferAMin9 = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example

# Set data buffers
# handle = chandle
# channel = channelA
# bufferMax = bufferAMax
# bufferMin = bufferAMin
# nSamples = nSamples
dataType = enums.PICO_DATA_TYPE["PICO_INT16_T"]
waveform = 0
downSampleMode = enums.PICO_RATIO_MODE["PICO_RATIO_MODE_RAW"]
clear = enums.PICO_ACTION["PICO_CLEAR_ALL"]
add = enums.PICO_ACTION["PICO_ADD"]
action = clear|add # PICO_ACTION["PICO_CLEAR_WAVEFORM_CLEAR_ALL"] | PICO_ACTION["PICO_ADD"]  
status["setDataBuffers"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), nSamples, dataType, waveform, downSampleMode, action)
assert_pico_ok(status["setDataBuffers"])
waveform1 = 1
status["setDataBuffers1"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax1), ctypes.byref(bufferAMin1), nSamples, dataType, waveform1, downSampleMode, add)
assert_pico_ok(status["setDataBuffers1"])
waveform2 = 2
status["setDataBuffers2"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax2), ctypes.byref(bufferAMin2), nSamples, dataType, waveform2, downSampleMode, add)
assert_pico_ok(status["setDataBuffers2"])
waveform3 = 3
status["setDataBuffers3"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax3), ctypes.byref(bufferAMin3), nSamples, dataType, waveform3, downSampleMode, add)
assert_pico_ok(status["setDataBuffers3"])
waveform4 = 4
status["setDataBuffers4"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax4), ctypes.byref(bufferAMin4), nSamples, dataType, waveform4, downSampleMode, add)
assert_pico_ok(status["setDataBuffers4"])
waveform5 = 5
status["setDataBuffers5"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax5), ctypes.byref(bufferAMin5), nSamples, dataType, waveform5, downSampleMode, add)
assert_pico_ok(status["setDataBuffers5"])
waveform6 = 6
status["setDataBuffers6"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax6), ctypes.byref(bufferAMin6), nSamples, dataType, waveform6, downSampleMode, add)
assert_pico_ok(status["setDataBuffers6"])
waveform7 = 7
status["setDataBuffers7"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax7), ctypes.byref(bufferAMin7), nSamples, dataType, waveform7, downSampleMode, add)
assert_pico_ok(status["setDataBuffers7"])
waveform8 = 8
status["setDataBuffers8"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax8), ctypes.byref(bufferAMin8), nSamples, dataType, waveform8, downSampleMode, add)
assert_pico_ok(status["setDataBuffers8"])
waveform9 = 9
status["setDataBuffers9"] = ps.psospaSetDataBuffers(chandle, channelA, ctypes.byref(bufferAMax9), ctypes.byref(bufferAMin9), nSamples, dataType, waveform9, downSampleMode, add)
assert_pico_ok(status["setDataBuffers9"])

# Run block capture
# handle = chandle
# timebase = timebase
timeIndisposedMs = ctypes.c_double(0)
# segmentIndex = 0
# lpReady = None   Using IsReady rather than a callback
# pParameter = None
status["runBlock"] = ps.psospaRunBlock(chandle, noOfPreTriggerSamples, noOfPostTriggerSamples, timebase, ctypes.byref(timeIndisposedMs), 0, None, None)
assert_pico_ok(status["runBlock"])

# Check for data collection to finish using psospaIsReady
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.psospaIsReady(chandle, ctypes.byref(ready))
    
# Get data from scope
# handle = chandle
# startIndex = 0
noOfSamples = ctypes.c_uint64(nSamples)
# downSampleRatio = 1
# segmentIndex = 0
# Creates a overflow location for each segment
overflow = (ctypes.c_int16 * 10)()
status["getValues"] = ps.psospaGetValuesBulk(chandle, 0, ctypes.byref(noOfSamples),0, 9, 1, downSampleMode, ctypes.byref(overflow))
assert_pico_ok(status["getValues"])

# convert ADC counts data to mV
adc2mVChAMax =  adc2mVV2(bufferAMax, rangeMax, maxADC)
adc2mVChAMax1 =  adc2mVV2(bufferAMax1, rangeMax, maxADC)
adc2mVChAMax2 =  adc2mVV2(bufferAMax2, rangeMax, maxADC)
adc2mVChAMax3 =  adc2mVV2(bufferAMax3, rangeMax, maxADC)
adc2mVChAMax4 =  adc2mVV2(bufferAMax4, rangeMax, maxADC)
adc2mVChAMax5 =  adc2mVV2(bufferAMax5, rangeMax, maxADC)
adc2mVChAMax6 =  adc2mVV2(bufferAMax6, rangeMax, maxADC)
adc2mVChAMax7 =  adc2mVV2(bufferAMax7, rangeMax, maxADC)
adc2mVChAMax8 =  adc2mVV2(bufferAMax8, rangeMax, maxADC)
adc2mVChAMax9 =  adc2mVV2(bufferAMax9, rangeMax, maxADC)

# Create time data
time = np.linspace(0, (nSamples -1) * timeInterval.value * 1000000000, nSamples)

# plot data from channel A and B
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

# Close the scope
status["closeunit"] = ps.psospaCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

print(status)