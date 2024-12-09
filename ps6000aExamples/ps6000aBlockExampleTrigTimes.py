#
# Copyright (C) 2020-2024 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 A BLOCK MODE EXAMPLE WITH ALL TRIGGER TIMES
# This example opens a 6000a driver device, sets up a channel A and its trigger then collects a block of data.
# This data is then plotted as mV against time in ns.
# Also the trigger data is plotted as mV against time in ns. (optional)
# Addition function calls so all trigger time values are returned correctly.

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
channelRange = 5
# analogueOffset = 0 V
bandwidth = enums.PICO_BANDWIDTH_LIMITER["PICO_BW_FULL"]
status["setChannelA"] = ps.ps6000aSetChannelOn(chandle, channelA, coupling, channelRange, 0, bandwidth)
assert_pico_ok(status["setChannelA"])

# set channel B-H off
for x in range (1, 3, 1):
    channel = x
    status["setChannel",x] = ps.ps6000aSetChannelOff(chandle,channel)
    assert_pico_ok(status["setChannel",x])
    
# get max ADC value
# handle = chandle
minADC = ctypes.c_int16()
maxADC = ctypes.c_int16()
status["getAdcLimits"] = ps.ps6000aGetAdcLimits(chandle, resolution, ctypes.byref(minADC), ctypes.byref(maxADC))
assert_pico_ok(status["getAdcLimits"])

# Set simple trigger on channel A, 1 V rising with 1 s autotrigger
# handle = chandle
# enable = 1
# threshold = 100 mV
direction = enums.PICO_THRESHOLD_DIRECTION["PICO_RISING"]
# delay = 0 s
# autoTriggerMicroSeconds = 1000000 us
status["setSimpleTrigger"] = ps.ps6000aSetSimpleTrigger(chandle, 1, channelA, mV2adc(0,channelRange,maxADC), direction, 0, 0)
assert_pico_ok(status["setSimpleTrigger"])

# Get fastest available timebase
# handle = chandle
enabledChannelFlags = enums.PICO_CHANNEL_FLAGS["PICO_CHANNEL_A_FLAGS"]
timebase = ctypes.c_uint32(0)
timeInterval = ctypes.c_double(0)
# resolution = resolution
status["getMinimumTimebaseStateless"] = ps.ps6000aGetMinimumTimebaseStateless(chandle, enabledChannelFlags, ctypes.byref(timebase), ctypes.byref(timeInterval), resolution)
print("MinimumTimebase is-")
print("timebase = ", timebase.value)
print("sample interval =", timeInterval.value, "s")

# Set number of samples to be collected
noOfPreTriggerSamples = 500000
noOfPostTriggerSamples = 500000
nSamples = noOfPostTriggerSamples + noOfPreTriggerSamples

# Create buffers
bufferAMax = (ctypes.c_int16 * nSamples)()
bufferAMin = (ctypes.c_int16 * nSamples)() # used for downsampling which isn't in the scope of this example

triggerSamples = 40 # This is always 40 - 20 samples around the trigger point.
triggerBuffer = (ctypes.c_int16 * triggerSamples)()

# Run block capture
# handle = chandle
# timebase = timebase
timeIndisposedMs = ctypes.c_double(0)
timebase = ctypes.c_uint32(50)

print("Setting Timebase of-")
print("timebase = ", timebase.value)

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
action = clear | add # PICO_ACTION["PICO_CLEAR_WAVEFORM_CLEAR_ALL"] | PICO_ACTION["PICO_ADD"] 

status["setDataBuffers"] = ps.ps6000aSetDataBuffers(chandle,
                                                    channelA,
                                                    ctypes.byref(bufferAMax),
                                                    ctypes.byref(bufferAMin),
                                                    nSamples,
                                                    dataType,
                                                    waveform,
                                                    downSampleMode,
                                                    action)

# Setup triggerSamples to get "trigger time offset" values when calling "GetTriggerInfo()" and "GetTriggerTimeOffset" functions.
status["setDataBuffers"] = ps.ps6000aSetDataBuffer(chandle,
                                                    channelA,
                                                    ctypes.byref(triggerBuffer),
                                                    ctypes.c_int32(triggerSamples),
                                                    dataType, 
                                                   waveform,
                                                    enums.PICO_RATIO_MODE["PICO_RATIO_MODE_TRIGGER"],
                                                    add)

assert_pico_ok(status["setDataBuffers"])

# Get data from scope
# handle = chandle
# startIndex = 0
noOfSamples = ctypes.c_uint64(nSamples)
# downSampleRatio = 1
# segmentIndex = 0
overflow = ctypes.c_int16(0)
status["getValues"] = ps.ps6000aGetValues(chandle, 0, ctypes.byref(noOfSamples), 1, downSampleMode, 0, ctypes.byref(overflow))
assert_pico_ok(status["getValues"])

# Request triggerSamples to get "trigger time offset" values when calling "GetTriggerInfo()" and "GetTriggerTimeOffset" functions. 
status["getValues"] = ps.ps6000aGetValues(chandle, 0, ctypes.byref(ctypes.c_uint64(triggerSamples)), noOfSamples, enums.PICO_RATIO_MODE["PICO_RATIO_MODE_TRIGGER"], 0, None)
assert_pico_ok(status["getValues"])

triggerInfo = (struct.PICO_TRIGGER_INFO * 1)()

status["GetTriggerInfo"] = ps.ps6000aGetTriggerInfo(chandle, ctypes.byref(triggerInfo), 0, 1)
assert_pico_ok(status["GetTriggerInfo"])
print("TimestampCounter values in samples (only relative timestamps one segment to the next)")
# print("Timestamp samples for 2nd segment (index 1, from segment 0 to 1) = ", triggerInfo(1).timeStampCounter)
print("Printing triggerInfo for segments-")
for i in triggerInfo:
    print("segmentIndex is ", i.segmentIndex)
    print("PICO_STATUS is ", i.status)
    print("triggerIndex is ", i.triggerIndex)
    print("triggerTime (jitter) is ", i.triggerTime)
    print("timeUnits is ", i.timeUnits)
    print("MissedTriggers is ", i.missedTriggers)
    print("timeStampCounter is ", i.timeStampCounter)
    print("-------------------------------")

timeGTO = ctypes.c_int64(0)
timeUnits = ctypes.c_uint32(0)
segmentIndex = ctypes.c_uint64(0)
 
status["GetTriggerTimeOffset"] = ps.ps6000aGetTriggerTimeOffset(chandle, ctypes.byref(timeGTO), ctypes.byref(timeUnits), segmentIndex)
assert_pico_ok(status["GetTriggerTimeOffset"])
print("Calling GetTriggerTimeOffset() -")
print("triggerTime (jitter) is ", timeGTO)
print("timeUnits is ", timeUnits)

# convert ADC counts data to mV
adc2mVChAMax =  adc2mV(bufferAMax, channelRange, maxADC)

# Create time data
time = np.linspace(0, (nSamples -1) * timeInterval.value * 1000000000, nSamples)

# plot data from channel A
plt.plot(time, adc2mVChAMax[:])
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (mV)')
plt.show()

# plot trigger area data
timetrigger = np.linspace(0, (triggerSamples -1) * timeInterval.value * 1000000000, triggerSamples)
plt.plot(timetrigger, triggerBuffer[:])
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (mV)')
plt.show()

# Close the scope
status["closeunit"] = ps.ps6000aCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

print(status)