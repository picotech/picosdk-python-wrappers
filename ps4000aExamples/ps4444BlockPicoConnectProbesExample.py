#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PS4444 PICOCONNECT PROBE, BLOCK MODE EXAMPLE
# This example opens a 4444 device, and demos PicoConnectProbes events.

import ctypes
from array import array
import time
import numpy as np
from picosdk.ps4000a import ps4000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok, adc2mVpl1000, mV2adcpl1000
from pynput import keyboard

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}
probes = (ps.PS4000A_USER_PROBE_INTERACTIONS * 4)()  #

# Calback for PicoConnectProbes events
def PicoConnectProbe_callback(handle, pico_status, probes_ptr, nProbes):
    global PicoConnectProbewasCalledBack
    PicoConnectProbewasCalledBack = True
    print("PicoConnectProbes pico_status ", pico_status)
    print("Number of PicoConnectProbes events is ", nProbes)
    #print(probes_ptr)

    # If probes_ptr is an integer (raw address), cast it to a pointer
    if isinstance(probes_ptr, int):
        probes_ptr = ctypes.cast(probes_ptr, ctypes.POINTER( (ps.PS4000A_USER_PROBE_INTERACTIONS) ))

    n_probes = nProbes
    if n_probes > 0 and probes_ptr:
        # Iterate over the pointer using the count provided by n_probes
        for i in range(n_probes):
            # Access the struct at index i
            probes[(probes_ptr[i].channel)] = probes_ptr[i]
    else:
        print("No probe interactions recorded.")

###########################################################
# Convert the python function into a C function pointer.
cFuncPtr2 = ps.ps4000aProbeInteractions(PicoConnectProbe_callback)

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

time.sleep(1.0) # Delay for first Probe callback events to trigger 

status["setChA"] = ps.ps4000aSetChannel(chandle, 0, 1, ps.PS4000A_COUPLING["PS4000A_DC"], ps.PICO_CONNECT_PROBE_RANGE["PICO_X1_PROBE_1V"], 0)
status["setChA"] = ps.ps4000aSetChannel(chandle, 1, 1, ps.PS4000A_COUPLING["PS4000A_DC"], ps.PICO_CONNECT_PROBE_RANGE["PICO_X1_PROBE_1V"], 0)
status["setChA"] = ps.ps4000aSetChannel(chandle, 2, 1, ps.PS4000A_COUPLING["PS4000A_DC"], ps.PICO_CONNECT_PROBE_RANGE["PICO_X1_PROBE_1V"], 0)
status["setChA"] = ps.ps4000aSetChannel(chandle, 3, 1, ps.PS4000A_COUPLING["PS4000A_DC"], ps.PICO_CONNECT_PROBE_RANGE["PICO_X1_PROBE_1V"], 0)

##################################################
# Look in \picosdk\ps4000a.py for all "PICO_CONNECT_PROBE_RANGE" defines for your Probe.

# The 4444 PicoConnect current clamps don't have auto zero offset.
# You need to manually set an analog offset in both PicoScope 7 and when using the API.
# If you measuring AC current you can just AC couple the channel to remove any offset.
# You can find out the max. and min. analogoffset values that can be set for any probe range by calling-
# ps4000aGetAnalogueOffset().

##################################################
print("Press 'Enter' to exit the Probe update loop!")
keep_going=keyboard.Listener(lambda key: False if key==keyboard.Key.enter else True)
keep_going.start()
while keep_going.is_alive():
    if (PicoConnectProbewasCalledBack == True):
        PicoConnectProbewasCalledBack = False
        print("DEBUG all probe status:")

        for i in range(4):
            #probe = probes_ptr[i]  # index into the array
            if (probes[i].connected):
                status["setChannel"] = ps.ps4000aSetChannel(chandle,
                                                            i, # channel
                                                            1, # enabled
                                                            ps.PS4000A_COUPLING["PS4000A_DC"], # coupling
                                                            (probes[i].rangeLast_), # probes[i].rangeFirst_, # ps.PICO_CONNECT_PROBE_RANGE[probes[i].rangeFirst_],
                                                            0) # offset
            else:
                status["setChannel"] = ps.ps4000aSetChannel(chandle, i, 0, ps.PS4000A_COUPLING["PS4000A_DC"], ps.PICO_CONNECT_PROBE_RANGE["PICO_CONNECT_PROBE_OFF"], 0)
            assert_pico_ok(status["setChannel"])
            
            #for i in range(4):
            print(f"Channel {i}:")
            print(f"  Connected: {probes[i].connected}")
            print(f"  probeName: {probes[i].probeName}")
            #print(f"  Status: {probes[i].status}")
            print(f"  Coupling: {probes[i].couplingCurrent_}")
                # Add more fields as needed      
    time.sleep(0.1)

#status["trigger"] = ps.ps4000aSetSimpleTrigger(chandle, 1, 0, 1024, 2, 0, 100)
#assert_pico_ok(status["trigger"])

# Set number of pre and post trigger samples to be collected
preTriggerSamples = 25000
postTriggerSamples = 25000
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
bufferCMax = (ctypes.c_int16 * maxSamples)()
bufferCMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example
bufferDMax = (ctypes.c_int16 * maxSamples)()
bufferDMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example

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

status["setDataBuffersB"] = ps.ps4000aSetDataBuffers(chandle, 1, ctypes.byref(bufferBMax), ctypes.byref(bufferBMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersB"])

status["setDataBuffersC"] = ps.ps4000aSetDataBuffers(chandle, 2, ctypes.byref(bufferCMax), ctypes.byref(bufferCMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersC"])

status["setDataBuffersD"] = ps.ps4000aSetDataBuffers(chandle, 3, ctypes.byref(bufferDMax), ctypes.byref(bufferDMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersD"])

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

# Scale for ps.PICO_CONNECT_PROBE_RANGE["PICO_CURRENT_CLAMP_40A_5A"] range -> scale to +/-5A
# adc2ProbeRangeChAMax = [(float(x) * 5 ) / float(maxADC.value) for x in float(bufferAMax)]
# Just use adc2mVpl1000() to do this, and pass the range value scale to.

# Just scale to 100 for percentage, for this demo
adc2ProbeRangeChAMax = adc2mVpl1000(bufferAMax, 100 , maxADC)
adc2ProbeRangeChBMax = adc2mVpl1000(bufferBMax, 100 , maxADC)
adc2ProbeRangeChCMax = adc2mVpl1000(bufferCMax, 100 , maxADC)
adc2ProbeRangeChDMax = adc2mVpl1000(bufferDMax, 100 , maxADC)
# NICE TO HAVE A FUNCTION AND LOOK TABLE/ARRAY TO TRANSLATE PROBE ENUMS TO SCALING VALUES, rather than passing in constant above.

# Create time data
time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)

# plot data
plt.plot(time, adc2ProbeRangeChAMax[:])
plt.plot(time, adc2ProbeRangeChBMax[:])
plt.plot(time, adc2ProbeRangeChCMax[:])
plt.plot(time, adc2ProbeRangeChDMax[:])

plt.xlabel('Time (ns)')
plt.ylabel('Channel range (+/-100%)')
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
