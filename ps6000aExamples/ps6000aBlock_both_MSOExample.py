#
# Copyright (C) 2020-2024 Pico Technology Ltd. See LICENSE file for terms.
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
from picosdk.functions import adc2mV, assert_pico_ok, splitMSODataFast

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 6000 A series PicoScope
# returns handle to chandle for use in future API functions
resolution = enums.PICO_DEVICE_RESOLUTION["PICO_DR_8BIT"]
status["openunit"] = ps.ps6000aOpenUnit(ctypes.byref(chandle), None, resolution)
assert_pico_ok(status["openunit"])

# set channel A-H off
for x in range (0, 7, 1):
    channel = x
    status["setChannel",x] = ps.ps6000aSetChannelOff(chandle,channel)
    assert_pico_ok(status["setChannel",x])
    
# set MSO pod 1 on
# handle = chandle
port_0 = enums.PICO_CHANNEL["PICO_PORT0"]
# logic level needs to be set individually for all digital channels/pins in the port
pins = 8
logicThresholdLevel = (ctypes.c_int16 * pins)(0)
logicThresholdLevel[0] = 6400 # ~1.5v
logicThresholdLevelLength = len(logicThresholdLevel)
hysteresis = enums.PICO_DIGITAL_PORT_HYSTERESIS["PICO_LOW_50MV"]
status["setDigitalPortOn"] = ps.ps6000aSetDigitalPortOn(chandle, 
                                                        port_0, 
                                                        ctypes.byref(logicThresholdLevel), 
                                                        logicThresholdLevelLength, 
                                                        hysteresis)
assert_pico_ok(status["setDigitalPortOn"])

# set MSO pod 2 on
# handle = chandle
port_1 = enums.PICO_CHANNEL["PICO_PORT1"]
# logic level needs to be set individually for all digital channels/pins in the port
pins = 8
logicThresholdLevel_upper = (ctypes.c_int16 * pins)(0)
logicThresholdLevel_upper[0] = 6400 #~1.5v
logicThresholdLevel_upperLength = len(logicThresholdLevel)
hysteresis = enums.PICO_DIGITAL_PORT_HYSTERESIS["PICO_LOW_50MV"]
status["setDigitalPortOn"] = ps.ps6000aSetDigitalPortOn(chandle, 
                                                        port_1, 
                                                        ctypes.byref(logicThresholdLevel_upper), 
                                                        logicThresholdLevel_upperLength, 
                                                        hysteresis)
assert_pico_ok(status["setDigitalPortOn"])

# Set trigger on digital channel 0 Port 1 for rising logic level transition 
conditions = (struct.PICO_CONDITION * 1)()
conditions = struct.PICO_CONDITION(enums.PICO_CHANNEL["PICO_PORT0"] , enums.PICO_TRIGGER_STATE["PICO_CONDITION_TRUE"])
nConditions = 1
clear = enums.PICO_ACTION["PICO_CLEAR_ALL"]
add = enums.PICO_ACTION["PICO_ADD"]
action = clear|add
action_post = add
status["setTriggerChannelConditions"] = ps.ps6000aSetTriggerChannelConditions(chandle, ctypes.byref(conditions),nConditions,action)
assert_pico_ok(status["setTriggerChannelConditions"])

directions = (struct.DIGITAL_CHANNEL_DIRECTIONS * 1)()
directions = struct.DIGITAL_CHANNEL_DIRECTIONS(enums.PICO_PORT_DIGITAL_CHANNEL["PICO_PORT_DIGITAL_CHANNEL0"],enums.PICO_DIGITAL_DIRECTION["PICO_DIGITAL_DIRECTION_RISING"])
nDirections = 1
status["setTriggerDigitalPortProperties"] = ps.ps6000aSetTriggerDigitalPortProperties(chandle,port_0,ctypes.byref(directions),nDirections)
assert_pico_ok(status["setTriggerDigitalPortProperties"])

# Set number of samples to be collected
noOfPreTriggerSamples = 25000
noOfPostTriggerSamples = 0
nSamples = noOfPostTriggerSamples + noOfPreTriggerSamples

# Check timebase is valid
# handle = chandle
timebase = ctypes.c_uint32(1)
timeInterval = ctypes.c_double(0)
returnedMaxSamples=ctypes.c_uint64()
#segment = 0
status["getTimebase"] = ps.ps6000aGetTimebase(chandle, timebase, nSamples, ctypes.byref(timeInterval), ctypes.byref(returnedMaxSamples), 0)
assert_pico_ok(status["getTimebase"])
print("timebase = ", timebase.value)
print("sample interval =", timeInterval.value, "ns")

# Create buffers
bufferDPort0 = (ctypes.c_int16 * nSamples)()
bufferDPort0Max = (ctypes.c_int16 * nSamples)()
bufferDPort0Min = (ctypes.c_int16 * nSamples)()

bufferDPort1 = (ctypes.c_int16 * nSamples)()
bufferDPort1Max = (ctypes.c_int16 * nSamples)()
bufferDPort1Min = (ctypes.c_int16 * nSamples)()

# Set data buffers
# handle = chandle
# channel = channelA
# bufferMax = bufferAMax
# bufferMin = bufferAMin
# nSamples = nSamples
dataType = enums.PICO_DATA_TYPE["PICO_INT16_T"]
#dataType_MSO = enums.PICO_DATA_TYPE["PICO_INT8_T"]

waveform = 0
downSampleMode = enums.PICO_RATIO_MODE["PICO_RATIO_MODE_RAW"]

status["setDataDP0Buffer"] = ps.ps6000aSetDataBuffers(chandle, 
                                                     port_0, 
                                                     ctypes.byref(bufferDPort0Max), 
                                                     ctypes.byref(bufferDPort0Min),
                                                     nSamples, 
                                                     dataType, 
                                                     waveform, 
                                                     downSampleMode, 
                                                     action)
assert_pico_ok(status["setDataDP0Buffer"])

status["setDataDP1Buffer"] = ps.ps6000aSetDataBuffers(
                                                    chandle, 
                                                    port_1, 
                                                    ctypes.byref(bufferDPort1Max), 
                                                    ctypes.byref(bufferDPort1Min),
                                                    nSamples, 
                                                    dataType, 
                                                    waveform, 
                                                    downSampleMode, 
                                                    action_post)
assert_pico_ok(status["setDataDP1Buffer"])

# Run block capture
# handle = chandle
# timebase = timebase
timeIndisposedMs = ctypes.c_double(0)
# segmentIndex = 0
# lpReady = None   Using IsReady rather than a callback
# pParameter = None
status["runBlock"] = ps.ps6000aRunBlock(
                                        chandle, 
                                        noOfPreTriggerSamples, 
                                        noOfPostTriggerSamples, 
                                        timebase, 
                                        ctypes.byref(timeIndisposedMs), 
                                        0, 
                                        None, 
                                        None)
assert_pico_ok(status["runBlock"])

# Check for data collection to finish using ps5000aIsReady
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
status["getValues"] = ps.ps6000aGetValues(
                                            chandle, 
                                            0, 
                                            ctypes.byref(noOfSamples), 
                                            1, 
                                            downSampleMode, 
                                            0, 
                                            ctypes.byref(overflow))
assert_pico_ok(status["getValues"])

# # Obtain binary for Digital Port 0
# # The tuple returned contains the channels in order (D7, D6, D5, ... D0).
# bufferDPort0 = splitMSODataFast(noOfSamples, bufferDPort0)
# bufferDPort1 = splitMSODataFast(noOfSamples, bufferDPort1)

# Obtain binary for Digital Port 0
# The tuple returned contains the channels in order (D7, D6, D5, ... D0).
bufferDPort0 = splitMSODataFast(noOfSamples, bufferDPort0Max)
bufferDPort1 = splitMSODataFast(noOfSamples, bufferDPort1Max)

# Create time data
time = np.linspace(0, (nSamples -1) * timeInterval.value * 1000000000, nSamples)

#MinMax plot
fig, axs = plt.subplots(2)
fig.suptitle("MSO data")

# Plot the data from digital channels onto a graph
axs[0].plot(time, bufferDPort0[0], label='D7')  # D7 is the first array in the tuple.
axs[0].plot(time, bufferDPort0[1], label='D6')
axs[0].plot(time, bufferDPort0[2], label='D5')
axs[0].plot(time, bufferDPort0[3], label='D4')
axs[0].plot(time, bufferDPort0[4], label='D3')
axs[0].plot(time, bufferDPort0[5], label='D2')
axs[0].plot(time, bufferDPort0[6], label='D1')
axs[0].plot(time, bufferDPort0[7], label='D0')  # D0 is the last array in the tuple.
axs[0].legend(loc="upper right")
#plt.show()

# Plot the data from digital channels onto a graph
axs[1].plot(time, bufferDPort1[0], label='D15')  # D7 is the first array in the tuple.
axs[1].plot(time, bufferDPort1[1], label='D14')
axs[1].plot(time, bufferDPort1[2], label='D13')
axs[1].plot(time, bufferDPort1[3], label='D12')
axs[1].plot(time, bufferDPort1[4], label='D11')
axs[1].plot(time, bufferDPort1[5], label='D10')
axs[1].plot(time, bufferDPort1[6], label='D9')
axs[1].plot(time, bufferDPort1[7], label='D8')  # D0 is the last array in the tuple.
axs[1].legend(loc="upper right")

plt.xlabel('Time (ns)')
plt.ylabel('Logic Level')
plt.show()


# fig, axs = plt.subplots(2)
# fig.suptitle("MSO data")

# # Plot the data from digital channels onto a graph
# axs[0].plot(time, bufferDPort0[0], label='D7')  # D7 is the first array in the tuple.
# axs[0].plot(time, bufferDPort0[1], label='D6')
# axs[0].plot(time, bufferDPort0[2], label='D5')
# axs[0].plot(time, bufferDPort0[3], label='D4')
# axs[0].plot(time, bufferDPort0[4], label='D3')
# axs[0].plot(time, bufferDPort0[5], label='D2')
# axs[0].plot(time, bufferDPort0[6], label='D1')
# axs[0].plot(time, bufferDPort0[7], label='D0')  # D0 is the last array in the tuple.
# axs[0].legend(loc="upper right")
# #plt.show()

# # Plot the data from digital channels onto a graph
# axs[1].plot(time, bufferDPort1[0], label='D15')  # D7 is the first array in the tuple.
# axs[1].plot(time, bufferDPort1[1], label='D14')
# axs[1].plot(time, bufferDPort1[2], label='D13')
# axs[1].plot(time, bufferDPort1[3], label='D12')
# axs[1].plot(time, bufferDPort1[4], label='D11')
# axs[1].plot(time, bufferDPort1[5], label='D10')
# axs[1].plot(time, bufferDPort1[6], label='D9')
# axs[1].plot(time, bufferDPort1[7], label='D8')  # D0 is the last array in the tuple.
# axs[1].legend(loc="upper right")

# plt.xlabel('Time (ns)')
# plt.ylabel('Logic Level')
# plt.show()

# Close the scope
status["closeunit"] = ps.ps6000aCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

print(status)