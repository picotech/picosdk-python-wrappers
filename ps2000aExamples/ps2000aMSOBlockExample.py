#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PicoScope 2000 Series (A API) MSO Block Mode Example
# This example demonstrates how to use the PicoScope 2000 Series (ps2000a) driver API functions in order to do the
# following:
#
# Open a connection to a PicoScope 2000 Series MSO device
# Setup input analog channels and a digital port
# Setup a trigger on a digital channel
# Collect a block of data
# Plot data

import ctypes
import numpy as np
from picosdk.ps2000a import ps2000a as ps, PS2000A_TRIGGER_CONDITIONS, PS2000A_DIGITAL_CHANNEL_DIRECTIONS
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, splitMSODataFast, assert_pico_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open a connection to a PicoScope 2000 Series device
# Returns handle to chandle for use in future API functions
status["openUnit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)
assert_pico_ok(status["openUnit"])

# Set up channel A
# handle = chandle
# channel = PS2000A_CHANNEL_A = 0
# enabled = 1
# coupling type = PS2000A_DC = 1
# range = PS2000A_2V = 7
# analogue offset = 0 V

channelA = ps.PS2000A_CHANNEL['PS2000A_CHANNEL_A']
chAEnabled = 1
chACoupling = ps.PS2000A_COUPLING['PS2000A_DC']
chARange = ps.PS2000A_RANGE['PS2000A_2V']
chAAnalogOffset = 0

status["setChA"] = ps.ps2000aSetChannel(chandle,
                                        channelA,
                                        chAEnabled,
                                        chACoupling,
                                        chARange,
                                        chAAnalogOffset)
assert_pico_ok(status["setChA"])

# Set up channel B
# handle = chandle
# channel = PS2000A_CHANNEL_B = 1
# enabled = 1
# coupling type = PS2000A_DC = 1
# range = PS2000A_2V = 7
# analogue offset = 0 V

channelB = ps.PS2000A_CHANNEL['PS2000A_CHANNEL_B']
chBEnabled = 1
chBCoupling = ps.PS2000A_COUPLING['PS2000A_DC']
chBRange = ps.PS2000A_RANGE['PS2000A_2V']
chBAnalogOffset = 0

status["setChB"] = ps.ps2000aSetChannel(chandle,
                                        channelB,
                                        chBEnabled,
                                        chBCoupling,
                                        chBRange,
                                        chBAnalogOffset)
assert_pico_ok(status["setChB"])

# Set Digital Port 0
# handle = chandle
# port = PS2000A_DIGITAL_PORT0 = 0x80
# enabled = 1
# logicLevel = 9754 (1.5 V)

dPort0 = ps.PS2000A_DIGITAL_PORT.get("PS2000A_DIGITAL_PORT0")
status["setDigitalPort0"] = ps.ps2000aSetDigitalPort(chandle, dPort0, 1, 9754)
assert_pico_ok(status["setDigitalPort0"])

# Set up trigger on digital channel
# Device will trigger when there is a transition from low to high on digital channel 0

# Set trigger conditions
# handle = chandle
# Trigger conditions:
# channelA            = PS2000A_CONDITION_DONT_CARE = 0
# channelB            = PS2000A_CONDITION_DONT_CARE = 0
# channelC            = PS2000A_CONDITION_DONT_CARE = 0
# channelD            = PS2000A_CONDITION_DONT_CARE = 0
# external            = PS2000A_CONDITION_DONT_CARE = 0
# aux                 = PS2000A_CONDITION_DONT_CARE = 0
# pulseWidthQualifier = PS2000A_CONDITION_DONT_CARE = 0
# digital             = PS2000A_CONDITION_TRUE = 1
# nConditions = 1

dont_care = ps.PS2000A_TRIGGER_STATE['PS2000A_CONDITION_DONT_CARE']
trigger_true = ps.PS2000A_TRIGGER_STATE['PS2000A_CONDITION_TRUE']
nConditions = 1

triggerConditions = PS2000A_TRIGGER_CONDITIONS(dont_care,
                                               dont_care,
                                               dont_care,
                                               dont_care,
                                               dont_care,
                                               dont_care,
                                               dont_care,
                                               trigger_true)

status["setTriggerChannelConditions"] = ps.ps2000aSetTriggerChannelConditions(chandle,
                                                                              ctypes.byref(triggerConditions),
                                                                              nConditions)
assert_pico_ok(status["setTriggerChannelConditions"])

# Set digital trigger directions

# handle = chandle
# Digital directions
# channel = PS2000A_DIGITAL_CHANNEL_0 = 0
# direction = PS2000A_DIGITAL_DIRECTION_RISING = 3
# nDirections = 1

digitalChannel = ps.PS2000A_DIGITAL_CHANNEL['PS2000A_DIGITAL_CHANNEL_0']
digiTriggerDirection = ps.PS2000A_DIGITAL_DIRECTION['PS2000A_DIGITAL_DIRECTION_RISING']

digitalDirections = PS2000A_DIGITAL_CHANNEL_DIRECTIONS(digitalChannel, digiTriggerDirection)
nDigitalDirections = 1

status["setTriggerDigitalPortProperties"] = ps.ps2000aSetTriggerDigitalPortProperties(chandle,
                                                                                      ctypes.byref(digitalDirections),
                                                                                      nDigitalDirections)
assert_pico_ok(status["setTriggerDigitalPortProperties"])

# Set number of pre- and post-trigger samples to be collected
preTriggerSamples = 2500
postTriggerSamples = 2500
totalSamples = preTriggerSamples + postTriggerSamples

# Get timebase information
# WARNING: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
# To access these Timebases, set any unused analogue channels to off.
# handle = chandle
# timebase = 1252 = 10000 ns = timebase (see Programmer's guide for more information on timebases)
# noSamples = totalSamples
# pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalNs)
# pointer to totalSamples = ctypes.byref(returnedMaxSamples)
# segment index = 0
timebase = 1252
timeIntervalNs = ctypes.c_float()
returnedMaxSamples = ctypes.c_int32()
oversample = ctypes.c_int16(0)

# Query this function in a loop in case the timebase index selected is invalid.

status["getTimebase2"] = ps.PICO_STATUS['PICO_INVALID_TIMEBASE']

while status["getTimebase2"] == ps.PICO_STATUS['PICO_INVALID_TIMEBASE']:

    status["getTimebase2"] = ps.ps2000aGetTimebase2(chandle,
                                                    timebase,
                                                    totalSamples,
                                                    ctypes.byref(timeIntervalNs),
                                                    oversample,
                                                    ctypes.byref(returnedMaxSamples),
                                                    0)

    if status["getTimebase2"] == ps.PICO_STATUS['PICO_OK']:
        break
    else:

        timebase = timebase + 1

assert_pico_ok(status["getTimebase2"])

print "Starting data collection - waiting for trigger on channel D0..."

# Run block capture
# handle = chandle
# number of pre-trigger samples = preTriggerSamples
# number of post-trigger samples = PostTriggerSamples
# timebase = 1252 = 10000 ns = timebase (see Programmer's guide for mre information on timebases)
# oversample = 0
# time indisposed ms = None (not needed in the example)
# segment index = 0
# lpReady = None (using ps2000aIsReady() rather than ps2000aBlockReady())
# pParameter = None
status["runBlock"] = ps.ps2000aRunBlock(chandle,
                                        preTriggerSamples,
                                        postTriggerSamples,
                                        timebase,
                                        oversample,
                                        None,
                                        0,
                                        None,
                                        None)
assert_pico_ok(status["runBlock"])

# Check for data collection to finish using ps2000aIsReady()
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)

while ready.value == check.value:
    status["isReady"] = ps.ps2000aIsReady(chandle, ctypes.byref(ready))

# Create buffers ready for assigning pointers for data collection
bufferA = (ctypes.c_int16 * totalSamples)()
bufferB = (ctypes.c_int16 * totalSamples)()
bufferDPort0 = (ctypes.c_int16 * totalSamples)()

ratio_mode_none = ps.PS2000A_RATIO_MODE['PS2000A_RATIO_MODE_NONE']

# Set data buffer location for data collection from channel A
# handle = chandle
# source = PS2000A_CHANNEL_A = 0
# pointer to buffer = ctypes.byref(bufferA)
# buffer length = totalSamples
# segment index = 0
# ratio mode = PS2000A_RATIO_MODE_NONE = 0
status["setDataBufferA"] = ps.ps2000aSetDataBuffer(chandle,
                                                   channelA,
                                                   ctypes.byref(bufferA),
                                                   totalSamples,
                                                   0,
                                                   ratio_mode_none)
assert_pico_ok(status["setDataBufferA"])

# Set data buffer location for data collection from channel B
# handle = chandle
# source = PS2000A_CHANNEL_B = 1
# pointer to buffer max = ctypes.byref(bufferB)
# buffer length = totalSamples
# segment index = 0
# ratio mode = PS2000A_RATIO_MODE_NONE = 0
status["setDataBufferB"] = ps.ps2000aSetDataBuffer(chandle,
                                                   channelB,
                                                   ctypes.byref(bufferB),
                                                   totalSamples,
                                                   0,
                                                   ratio_mode_none)
assert_pico_ok(status["setDataBufferB"])

# Set data buffer location for data collection from digital port 0
# handle = chandle
# source = PS2000A_DIGITAL_PORT0 = 0x80
# pointer to buffer max = ctypes.byref(bufferB)
# buffer length = totalSamples
# segment index = 0
# ratio mode = PS2000A_RATIO_MODE_NONE = 0
status["setDataBufferDPort0"] = ps.ps2000aSetDataBuffer(chandle,
                                                        dPort0,
                                                        ctypes.byref(bufferDPort0),
                                                        totalSamples,
                                                        0,
                                                        ratio_mode_none)
assert_pico_ok(status["setDataBufferDPort0"])

# create overflow location
overflow = ctypes.c_int16()
# create converted type totalSamples
cTotalSamples = ctypes.c_int32(totalSamples)

# Retried data from scope to buffers assigned above
# handle = chandle
# start index = 0
# pointer to number of samples = ctypes.byref(cTotalSamples)
# downsample ratio = 1
# downsample ratio mode = PS2000A_RATIO_MODE_NONE
# pointer to overflow = ctypes.byref(overflow))
status["getValues"] = ps.ps2000aGetValues(chandle,
                                          0,
                                          ctypes.byref(cTotalSamples),
                                          0,
                                          1,
                                          ratio_mode_none,
                                          ctypes.byref(overflow))
assert_pico_ok(status["getValues"])

print "Data collection complete."

# Find maximum ADC count value
# handle = chandle
# pointer to value = ctypes.byref(maxADC)
maxADC = ctypes.c_int16()
status["maximumValue"] = ps.ps2000aMaximumValue(chandle, ctypes.byref(maxADC))
assert_pico_ok(status["maximumValue"])

# Convert ADC counts data to millivolts
adc2mVChA = adc2mV(bufferA, chARange, maxADC)
adc2mVChB = adc2mV(bufferB, chBRange, maxADC)

# Obtain binary for Digital Port 0
# The tuple returned contains the channels in order (D7, D6, D5, ... D0).
dPort0BinaryData = splitMSODataFast(cTotalSamples, bufferDPort0)

# Create time data
time = np.linspace(0, (cTotalSamples.value - 1) * timeIntervalNs.value, cTotalSamples.value)

# Plot data from channels A, B and D0

print "Plotting data..."

fig, axs = plt.subplots(2, 1, constrained_layout=True)
axs[0].plot(time, adc2mVChA[:], time, adc2mVChB[:])
axs[0].set_title('Analog data acquisition')
axs[0].set_xlabel('Time (ns)')
axs[0].set_ylabel('Voltage (mV)')
axs[0].legend(('Ch. A', 'Ch. B'), loc="upper right")

axs[1].plot(time, dPort0BinaryData[7], label='D0')  # D0 is the last array in the tuple.
axs[1].set_title('Digital data acquisition')
axs[1].set_xlabel('Time (ns)')
axs[1].set_ylabel('Logic Level')
axs[1].legend(loc="upper right")

fig.canvas.set_window_title('PicoScope 2000 Series (A API) MSO Block Capture Example')
plt.show()

print "Close figure to stop the device and close the connection."

# Stop the scope
# handle = chandle
status["stop"] = ps.ps2000aStop(chandle)
assert_pico_ok(status["stop"])

# Close the connection to the device
# handle = chandle
status["close"] = ps.ps2000aCloseUnit(chandle)
assert_pico_ok(status["close"])

# display status returns
print(status)
