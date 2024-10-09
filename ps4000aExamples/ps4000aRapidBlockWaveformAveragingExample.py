#
# Copyright (C) 2020-2024 Pico Technology Ltd. See LICENSE file for terms.
#
# PS4000 A BLOCK MODE WAVEFORM AVERAGING EXAMPLE
# This example opens a 4000a driver device, sets up two channels and a trigger then collects blocks of data.
# The blocks are then avraged together for each channel.
# This data is then plotted as mV against time in ns.

import ctypes
import numpy as np
from picosdk.ps4000a import ps4000a as ps
from picosdk.PicoDeviceEnums import picoEnum as enums
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok, mV2adc
from picosdk.functionsExhibitions import *
from math import ceil

# Scope settings
noOfChannels = 1
samplingRate = 1 #Mhz 
sampleLength = 10000 #Samples
numberOfSegments = 10

timebase = ps4000aTimebase(samplingRate)


# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 6000 A series PicoScope
# returns handle to chandle for use in future API functions
status["openunit"] = ps.ps4000aOpenUnit(ctypes.byref(chandle), None)
try:
    assert_pico_ok(status["openunit"])
except: # PicoNotOkError:

    powerStatus = status["openunit"]

    if powerStatus == 286:
        status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
    elif powerStatus == 282:
        status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
    else:
        raise

    assert_pico_ok(status["changePowerSource"])

# Set channels on
# handle = chandle
coupling = enums.PICO_COUPLING["PICO_DC"]
channelRange = 7 # +-2 V range
# analogueOffset = 0 V

for x in range(0, noOfChannels, 1):
    channel = x
    status["setChannel",x] = ps.ps4000aSetChannel(chandle, channel, 1, coupling, channelRange, 0)
    assert_pico_ok(status["setChannel",x])
    
# set channels off
for x in range (noOfChannels, 4, 1):
    channel = x
    status["setChannel",x] = ps.ps4000aSetChannel(chandle,channel, 0, coupling, channelRange, 0)
    try:
        assert_pico_ok(status["setChannel",x])
    except:
        break
    
# get max ADC value
# handle = chandle
maxADC = ctypes.c_int16()
status["getAdcLimits"] = ps.ps4000aMaximumValue(chandle, ctypes.byref(maxADC))
assert_pico_ok(status["getAdcLimits"])

# Set simple trigger on channel A, 1 V rising with 1 s autotrigger
# handle = chandle
# enable = 1
source = 0
# threshold = 100 mV
direction = enums.PICO_THRESHOLD_DIRECTION["PICO_RISING"]
# delay = 0 s
# autoTriggerMicroSeconds = 1000000 us
status["setSimpleTrigger"] = ps.ps4000aSetSimpleTrigger(chandle, 1, source, (mV2adc(500,channelRange,maxADC)), direction, 0, 1000000)
assert_pico_ok(status["setSimpleTrigger"])

# Set number of samples to be collected
noOfPreTriggerSamples = int(sampleLength/2)
noOfPostTriggerSamples = int(sampleLength/2)
nSamples = int(noOfPostTriggerSamples + noOfPreTriggerSamples)

# Get fastest available timebase
# handle = chandle
# enabledChannelFlags = enums.PICO_CHANNEL_FLAGS["PICO_CHANNEL_A_FLAGS"]
# timebase = ctypes.c_uint32(0)
timeInterval = ctypes.c_float(0)
# # resolution = resolution
# status["getMinimumTimebaseStateless"] = ps.ps4000aGetMinimumTimebaseStateless(chandle, enabledChannelFlags, ctypes.byref(timebase), ctypes.byref(timeInterval), resolution)
# print("timebase = ", timebase.value)
# print("sample interval =", timeInterval.value, "s")
maxSamples = ctypes.c_uint32(0)

status["getTimebase"] = ps.ps4000aGetTimebase2(chandle, timebase, nSamples, ctypes.byref(timeInterval), ctypes.byref(maxSamples), 0)
assert_pico_ok(status["getTimebase"])

# Set number of memory segments
maxSegments = ctypes.c_uint64(10)
status["memorySegments"] = ps.ps4000aMemorySegments(chandle, numberOfSegments, ctypes.byref(maxSegments))
assert_pico_ok(status["memorySegments"])

# Set number of captures
status["setNoOfCaptures"] = ps.ps4000aSetNoOfCaptures(chandle, numberOfSegments)
assert_pico_ok(status["setNoOfCaptures"])

oneDBuffer = (ctypes.c_int16 * nSamples)
twoDbuffer = (oneDBuffer * numberOfSegments)
threeDBuffer = (twoDbuffer * noOfChannels)
buffer = (threeDBuffer)()

# Set data buffers
# handle = chandle
# channel = channelA
# bufferMax = bufferAMax
# bufferMin = bufferAMin
# nSamples = nSamples
downSampleMode = ps.PS4000A_RATIO_MODE["PS4000A_RATIO_MODE_NONE"]


for x in range(0, numberOfSegments, 1):
    for y in range(0, noOfChannels, 1):
        channel = y
        status["setDataBuffers",x,y] = ps.ps4000aSetDataBuffer(chandle, channel, ctypes.byref(buffer[y][x]), nSamples, x, downSampleMode)
        assert_pico_ok(status["setDataBuffers",x,y])


# sign gen output
# Set signal generator waveform
# handle = chandle
# offsetVoltage = 0
# pkToPk = 2000000
wavetype = ctypes.c_int32(0) #PS4000a_SINE
frequencyHz = 1000
# increment = 0
# dwellTime = 1
sweepType = ctypes.c_int32(0) #PS4000a_UP
# operation = 0
# shots = 0
# sweeps = 0
triggertype = ctypes.c_int32(0) #PS4000a_SIGGEN_RISING
triggerSource = ctypes.c_int32(0) #P4000a_SIGGEN_NONE
# extInThreshold = 1
status["setSigGenBuiltInV2"] = ps.ps4000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, frequencyHz, frequencyHz, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 0)
assert_pico_ok(status["setSigGenBuiltInV2"])

# Run block capture
# handle = chandle
# timebase = timebase
timeIndisposedMs = ctypes.c_double(0)
# segmentIndex = 0
# lpReady = None   Using IsReady rather than a callback
# pParameter = None
status["runBlock"] = ps.ps4000aRunBlock(chandle, noOfPreTriggerSamples, noOfPostTriggerSamples, timebase, ctypes.byref(timeIndisposedMs), 0, None, None)
assert_pico_ok(status["runBlock"])

# Check for data collection to finish using ps4000aIsReady
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.ps4000aIsReady(chandle, ctypes.byref(ready))

# Get data from scope
# handle = chandle
# startIndex = 0
noOfSamples = ctypes.c_uint64(nSamples)
# downSampleRatio = 1
# segmentIndex = 0
# Creates a overflow location for each segment
overflow = (ctypes.c_int16 * numberOfSegments)()
status["getValues"] = ps.ps4000aGetValuesBulk(chandle, ctypes.byref(noOfSamples), 0, numberOfSegments-1, 1, downSampleMode, ctypes.byref(overflow))
assert_pico_ok(status["getValues"])

oneDBuffer = (ctypes.c_float * nSamples)
twoDbuffer = (oneDBuffer * numberOfSegments)
threeDBuffer = (twoDbuffer * noOfChannels)
rapidBlockBuffers = (threeDBuffer)()

# convert ADC counts data to mV
# convert all active channels
for x in range (0, numberOfSegments,1):
    for y in range (0, noOfChannels, 1):
        A =  adc2mV(buffer[y][x], channelRange, maxADC)
        for z in range(0, nSamples, 1):
            rapidBlockBuffers[y][x][z] = ctypes.c_float(A[z]) 

# Average waveforms
averageWaveform=np.zeros((noOfChannels,nSamples))

# loop through each channel, each memory segment and each sample to sum together, then divides by the number of memory segment to get the mean waveform for each channel
for y in range (0, noOfChannels, 1):
    for x in range (0, numberOfSegments,1):
        for z in range (0, nSamples,1):
            averageWaveform[y][z] = averageWaveform[y][z] + rapidBlockBuffers[y][x][z]
    averageWaveform[y] = [x/numberOfSegments for x in averageWaveform[y]]

# Create time data
time = np.linspace(0, (nSamples -1) * timeInterval.value * 1000000000, nSamples)

# plot channel A from all blocks
# for y in range (0, numberOfSegments, 1):
    # segment = y
    # plt.plot(time, rapidBlockBuffers[0][y])
    
# plot averaged waveform from channel A
plt.plot(time, averageWaveform[0])
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (mV)')
plt.show()

# Close the scope
status["closeunit"] = ps.ps4000aCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

print(status)