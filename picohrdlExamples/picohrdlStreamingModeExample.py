#
# Copyright (C) 2025 Pico Technology Ltd. See LICENSE file for terms.
#
# PICOLOG HIGH RESOLUTION DATA LOGGER STREAMING MODE EXAMPLE
#
# This example demonstrates how to capture data streaming from an ADC-20 or ADC-24 Precision Data Logger.

import ctypes
import numpy as np
from picosdk.picohrdl import picohrdl as hrdl
from picosdk.functions import assert_pico2000_ok
import matplotlib.pyplot as plt
import time

# Create chandle and status ready for use
chandle = ctypes.c_int16(16384)
status = {}
maxSamples = 200 #1_000

status["closeUnit"] = hrdl.HRDLCloseUnit(chandle)

# Open unit
status["openUnit"] = hrdl.HRDLOpenUnit()
assert_pico2000_ok(status["openUnit"])
chandle = status["openUnit"]

# Set mains noise rejection
# Reject 50 Hz mains noise
status["mainsRejection"] = hrdl.HRDLSetMains(chandle, 0)
assert_pico2000_ok(status["mainsRejection"])

# Setup Channel(s)
range = ctypes.c_int16(0)
range = hrdl.HRDL_VOLTAGERANGE["HRDL_2500_MV"]
overflow = ctypes.c_int16(0)
value = ctypes.c_int32()

channel = ctypes.c_int16(1) # (Ch number) ADC-20: Ch1 to Ch8 , ADC-24: Ch1 to Ch16
enabled = ctypes.c_int16(1)
singleEnded = ctypes.c_int16(1) # 0: differential, Not 0: for single ended

status["SetAnalogInChannel"] = hrdl.HRDLSetAnalogInChannel(chandle, channel, enabled, range, singleEnded)
assert_pico2000_ok(status["SetAnalogInChannel"])

# Streaming
# sampleInterval_ms = conversionTime x NumberOfChannels + 20ms
# 20ms = 1/3 of the fastest sample time for one channel
sampleInterval_ms = ctypes.c_int32(100 * 1 + 20)
conversionTime = hrdl.HRDL_CONVERSIONTIME["HRDL_100MS"]
status["SetInterval"] = hrdl.HRDLSetInterval(chandle, sampleInterval_ms, conversionTime)
assert_pico2000_ok(status["SetInterval"])

nValues = ctypes.c_int32(20)
method = ctypes.c_int16(2) # BM_STREAM (2)
status["Run"] = hrdl.HRDLRun(chandle, nValues, method)
assert_pico2000_ok(status["Run"])

TotalValues = 0
# Buffers
TempBuffer = (ctypes.c_int32 * 100)()
BufValues = []

myready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
# Check for data collection
while TotalValues < maxSamples:
    while myready.value == check.value:
        myready.value = hrdl.HRDLReady(chandle)
        time.sleep(0.02) # 20ms = 1/3 of the fastest sample time for one channel
        # print("ready = ", myready) # DEBUG
    noOfValues = ctypes.c_int32(20) # Ask for 20 samples
    noOfValues = hrdl.HRDLGetValues(chandle, ctypes.byref(TempBuffer), ctypes.byref(overflow), noOfValues)  
    TotalValues = TotalValues + int(noOfValues)
    print("TotalValues = ",TotalValues ,", noOfValues = ", int(noOfValues) ) # DEBUG
    #sleep (sampleInterval_ms - 20ms /1000)
    time.sleep( ((100 * 1 + 20) - 20) /1000)

    #for i in range(noOfValues):
        ####TempBuffer[i] =  adc2mV(TempBuffer[i], channelRange, maxADC)
        #BufValues.append(float(TempBuffer[i]))
    #if(noOfValues != 0):
    #    BufValues.append(float(TempBuffer[0]))

    # Convert to mV and Append values App Buffer
    loop = noOfValues
    while (loop != 0):
        loop = loop -1
        # TempBuffer[loop] =  adc2mVpl1000(TempBuffer[loop], 2500, 8388607) # adc2mVpl1000(value, Max range in mV, Max ADC count)
        #TempBuffer[loop] = (TempBuffer[loop] * 2500) / 8388607
        BufValues.append(float((TempBuffer[loop] * 2500) / 8388607))

# Stop data collection
hrdl.HRDLStop(chandle)

# Create time data
timeMs = np.linspace(0, (len(BufValues) -1) * 0.1, len(BufValues))

# plot data
plt.plot(timeMs, BufValues[:])
plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)')
plt.show()

# Close unit
status["closeUnit"] = hrdl.HRDLCloseUnit(chandle)
assert_pico2000_ok(status["closeUnit"])

# Print status
print(status)