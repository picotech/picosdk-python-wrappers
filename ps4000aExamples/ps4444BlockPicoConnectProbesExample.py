#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PS4824 BLOCK MODE EXAMPLE
# This example opens a 4000a driver device, sets up two channels and a trigger then collects a block of data.
# This data is then plotted as mV against time in ns.

import ctypes
from array import array
import time
import numpy as np
from picosdk.ps4000a import ps4000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok, adc2mVpl1000, mV2adcpl1000

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Calback for PicoConnectProbes events
def PicoConnectProbe_callback(handle, pico_status, probes, nProbes):
    global PicoConnectProbewasCalledBack
    PicoConnectProbewasCalledBack = True

    print("Number of PicoConnectProbes events is ", nProbes)

    probeUpdates = (ps.PS4000A_USER_PROBE_INTERACTIONS*nProbes) ()
    probeUpdates = ctypes.byref(probes)

    # Create array of ps.PS4000A_USER_PROBE_INTERACTIONS for each of the 4 channels
    four_PS4000AUserProbeInfo = (ps.PS4000A_USER_PROBE_INTERACTIONS*4) ()

    # Copy probeUpdates to matching channels in four_PS4000AUserProbeInfo
    for i in probeUpdates:
        four_PS4000AUserProbeInfo[probeUpdates[i].channel] = probeUpdates[i]

    # DEBUG to print out current/last probe stat on each channel
    for i in four_PS4000AUserProbeInfo:
        print("Channel is ", i.channel)
        print("PICO_STATUS is ", i.status)
        print("Eabled is ", i.enable)
        print("Connected is ", i.connected)
        print("Current Range is ", i.rangeCurrent_)  
    #WORK IN PROCESS!

# Convert the python function into a C function pointer.
cFuncPtr2 = ps.StreamingReadyType(PicoConnectProbe_callback)

# Open 4000 series PicoScope
# Returns handle to chandle for use in future API functions
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

status["SetProbeInteractionCallback"] = ps.ps4000aSetProbeInteractionCallback(chandle, cFuncPtr2)
assert_pico_ok(status["SetProbeInteractionCallback"])

time.sleep(4) # Delay for first Probe callback events to trigger 

# Set up channel A
# handle = chandle
# channel = PS4000a_CHANNEL_A = 0
# enabled = 1
# coupling type = PS4000a_DC = 1
# range = PS4000a_2V = 7
# analogOffset = 0 V
# chARange = 7
# chARange = ps.PICO_CONNECT_PROBE_RANGE["PICO_CURRENT_CLAMP_40A_5A"]
chARange = ps.PICO_CONNECT_PROBE_RANGE["PICO_CURRENT_CLAMP_200A_2KA_5A"] # pico_current_clamp_200a_2ka_5a
# Look in \picosdk\ps4000a.py for all "PICO_CONNECT_PROBE_RANGE" defines for your Probe.

# The 4444 PicoConnect current clamps don't have auto zero offset.
# You need to manually set an analog offset in both PicoScope 7 and when using the API.
# If you measuring AC current you can just AC couple the channel to remove any offset.
# You can find out the max. and min. analogoffset values that can be set for any probe range by calling-
# ps4000aGetAnalogueOffset().
status["setChA"] = ps.ps4000aSetChannel(chandle, 0, 1, 1, chARange, 0)
assert_pico_ok(status["setChA"])

# Set up channel B
# handle = chandle
# channel = PS4000a_CHANNEL_B = 1
# enabled = 1
# coupling type = PS4000a_DC = 1
# range = PS4000a_2V = 7
# analogOffset = 0 V
chBRange = 7
status["setChB"] = ps.ps4000aSetChannel(chandle, 1, 1, 1, chBRange, 0)
assert_pico_ok(status["setChB"])

# Set up channel C
# handle = chandle
# channel = PS4000a_CHANNEL_C = 2
# enabled = 1
# coupling type = PS4000a_DC = 1
# range = PS4000a_2V = 7
# analogOffset = 0 V
chCRange = 7
status["setChC"] = ps.ps4000aSetChannel(chandle, 2, 0, 1, chCRange, 0)
assert_pico_ok(status["setChC"])

# Set up channel D
# handle = chandle
# channel = PS4000a_CHANNEL_D = 3
# enabled = 1
# coupling type = PS4000a_DC = 1
# range = PS4000a_2V = 7
# analogOffset = 0 V
chDRange = 7
status["setChD"] = ps.ps4000aSetChannel(chandle, 3, 0, 1, chDRange, 0)
assert_pico_ok(status["setChD"])

# Set up single trigger
# handle = chandle
# enabled = 1
# source = PS4000a_CHANNEL_A = 0
# threshold = 1024 ADC counts
# direction = PS4000a_RISING = 2
# delay = 0 s
# auto Trigger = 1000 ms
status["trigger"] = ps.ps4000aSetSimpleTrigger(chandle, 1, 0, 1024, 2, 0, 100)
assert_pico_ok(status["trigger"])

# Set number of pre and post trigger samples to be collected
preTriggerSamples = 2500
postTriggerSamples = 2500
maxSamples = preTriggerSamples + postTriggerSamples

# Get timebase information
# handle = chandle
# timebase = 8 = timebase
# noSamples = maxSamples
# pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalns)
# pointer to maxSamples = ctypes.byref(returnedMaxSamples)
# segment index = 0
timebase = 400
timeIntervalns = ctypes.c_float()
returnedMaxSamples = ctypes.c_int32()
oversample = ctypes.c_int16(1)
status["getTimebase2"] = ps.ps4000aGetTimebase2(chandle, timebase, maxSamples, ctypes.byref(timeIntervalns), ctypes.byref(returnedMaxSamples), 0)
assert_pico_ok(status["getTimebase2"])

# Run block capture
# handle = chandle
# number of pre-trigger samples = preTriggerSamples
# number of post-trigger samples = PostTriggerSamples
# timebase = 3 = 80 ns = timebase (see Programmer's guide for mre information on timebases)
# time indisposed ms = None (not needed in the example)
# segment index = 0
# lpReady = None (using ps4000aIsReady rather than ps4000aBlockReady)
# pParameter = None
status["runBlock"] = ps.ps4000aRunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, None, 0, None, None)
assert_pico_ok(status["runBlock"])

# Check for data collection to finish using ps4000aIsReady
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.ps4000aIsReady(chandle, ctypes.byref(ready))

# Create buffers ready for assigning pointers for data collection
bufferAMax = (ctypes.c_int16 * maxSamples)()
bufferAMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example
bufferBMax = (ctypes.c_int16 * maxSamples)()
bufferBMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example

# Set data buffer location for data collection from channel A
# handle = chandle
# source = PS4000a_CHANNEL_A = 0
# pointer to buffer max = ctypes.byref(bufferAMax)
# pointer to buffer min = ctypes.byref(bufferAMin)
# buffer length = maxSamples
# segementIndex = 0
# mode = PS4000A_RATIO_MODE_NONE = 0
status["setDataBuffersA"] = ps.ps4000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersA"])

# Set data buffer location for data collection from channel B
# handle = chandle
# source = PS4000a_CHANNEL_B = 1
# pointer to buffer max = ctypes.byref(bufferBMax)
# pointer to buffer min = ctypes.byref(bufferBMin)
# buffer length = maxSamples
# segementIndex = 0
# mode = PS4000A_RATIO_MODE_NONE = 0
status["setDataBuffersB"] = ps.ps4000aSetDataBuffers(chandle, 1, ctypes.byref(bufferBMax), ctypes.byref(bufferBMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersB"])

# create overflow loaction
overflow = ctypes.c_int16()
# create converted type maxSamples
cmaxSamples = ctypes.c_int32(maxSamples)

# Retried data from scope to buffers assigned above
# handle = chandle
# start index = 0
# pointer to number of samples = ctypes.byref(cmaxSamples)
# downsample ratio = 0
# downsample ratio mode = PS4000a_RATIO_MODE_NONE
# pointer to overflow = ctypes.byref(overflow))
status["getValues"] = ps.ps4000aGetValues(chandle, 0, ctypes.byref(cmaxSamples), 0, 0, 0, ctypes.byref(overflow))
assert_pico_ok(status["getValues"])


# find maximum ADC count value
# handle = chandle
# pointer to value = ctypes.byref(maxADC)
maxADC = ctypes.c_int16(32767)

# convert ADC counts data to mV
# adc2mVChAMax =  adc2mV(bufferAMax, chARange, maxADC)
# adc2mVChBMax =  adc2mV(bufferBMax, chBRange, maxADC)

adc2mVChAMax = bufferAMax # Just copy ADC values for now

# Scale for ps.PICO_CONNECT_PROBE_RANGE["PICO_CURRENT_CLAMP_40A_5A"] range -> scale to +/-5A
# adc2ProbeRangeChAMax = [(float(x) * 5 ) / float(maxADC.value) for x in float(bufferAMax)]
# Just use adc2mVpl1000() to do this, and pass the range value scale to.
adc2ProbeRangeChAMax = adc2mVpl1000(bufferAMax, 5 , maxADC)

# NICE TO HAVE A FUNCTION AND LOOK TABLE/ARRAY TO TRANSLATE PROBE ENUMS TO SCALING VALUES, rather than passing in constant above.

# Create time data
time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)

# plot data from channel A
# plt.plot(time, bufferAMax[:])
plt.plot(time, adc2ProbeRangeChAMax[:])

# plt.plot(time, adc2mVChBMax[:])

plt.xlabel('Time (ns)')
plt.ylabel('Channel range units (?)')
plt.show()

# Stop the scope
# handle = chandle
status["stop"] = ps.ps4000aStop(chandle)
assert_pico_ok(status["stop"])

# Close unitDisconnect the scope
# handle = chandle
status["close"] = ps.ps4000aCloseUnit(chandle)
assert_pico_ok(status["close"])

# display status returns
print(status)
