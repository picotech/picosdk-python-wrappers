#
# Copyright (C) 2022 Pico Technology Ltd. See LICENSE file for terms.
#
# PT104 Example
# This example opens a pt104, sets up a single channel and collects data before closing the pt104

import ctypes
from picosdk.usbPT104 import usbPt104 as pt104
import numpy as np
from picosdk.functions import assert_pico_ok
from time import sleep
import matplotlib.pyplot as plt

# Create chandle and status ready for use
status = {}
chandle = ctypes.c_int16()

# Open the device
status["openUnit"] = pt104.UsbPt104OpenUnit(ctypes.byref(chandle),0)
assert_pico_ok(status["openUnit"])

# Set mains noise filtering
sixty_hertz = 0 #50 Hz
status["setMains"] = pt104.UsbPt104SetMains(chandle, sixty_hertz)
assert_pico_ok(status["setMains"])

# Setup channel 1
channel = pt104.PT104_CHANNELS["USBPT104_CHANNEL_1"] #channel 1
datatype = pt104.PT104_DATA_TYPE["USBPT104_PT100"] #pt100
noOfWires = 4 #wires

status["setChannel1"] = pt104.UsbPt104SetChannel(chandle, channel, datatype, noOfWires)
assert_pico_ok(status["setChannel1"])

#collect data
print("collecting data")
numSamples = 20

data = (ctypes.c_int32 * numSamples)()

for i in range(numSamples):

    #pause
    sleep(2)

    # Get values
    measurement = ctypes.c_int32()
    filtered = 1 # true
    status["getValue"] = pt104.UsbPt104GetValue(chandle, channel, ctypes.byref(measurement), filtered)
    assert_pico_ok(status["getValue"])
    
    data[i] = measurement.value

samples = np.linspace(0, numSamples*2, numSamples)
dataTemp = [x /1000 for x in data]   

plt.plot(samples, dataTemp)
plt.xlabel('Time (s)')
plt.ylabel('Temperature ($^o$C)')
plt.show()

# Close the device
status["closeUnit"] = pt104.UsbPt104CloseUnit(chandle)
assert_pico_ok(status["closeUnit"])

print(status)