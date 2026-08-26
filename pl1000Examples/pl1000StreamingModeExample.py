#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# PL1000 STREAMING MODE EXAMPLE
# This example opens a PicoLog 1000 device, configures streaming mode to capture data from channel 1 at
# a sampling rate of 100 kS/s for 10 seconds, retrieves the data, and displays it on a plot.

import ctypes
import numpy as np
from picosdk.pl1000 import pl1000 as pl
import matplotlib.pyplot as plt
from picosdk.functions import adc2mVpl1000, assert_pico_ok
from time import sleep

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open PicoLog 1000 device
status["openUnit"] = pl.pl1000OpenUnit(ctypes.byref(chandle))
assert_pico_ok(status["openUnit"])

# Everything after the unit is open runs inside try/finally so the unit is
# always stopped and released, including when a call fails and assert_pico_ok
# raises. Without this a failure part-way through left the device streaming.
try:
    # set sampling interval
    # 1,000,000 samples over 10 s on one channel is 100 kS/s.
    requestedSamples = 1000000
    usForBlock = ctypes.c_uint32(10000000)

    # The driver expects an array of channel numbers, one per enabled channel.
    channels = (ctypes.c_int16 * 1)(pl.PL1000Inputs["PL1000_CHANNEL_1"])

    status["setInterval"] = pl.pl1000SetInterval(chandle, ctypes.byref(usForBlock), requestedSamples, channels, 1)
    assert_pico_ok(status["setInterval"])

    # start streaming
    # In BM_STREAM mode the count passed to pl1000Run is the size of the
    # driver's circular buffer, in samples per channel - not the number of
    # samples to collect. Sizing it to exactly the collection period leaves no
    # headroom, so readings at the start can be overwritten before they are
    # read. The pl1000Con C example uses a factor of ten for the same reason.
    circularBufferSamples = requestedSamples * 2
    mode = pl.PL1000_BLOCK_METHOD["BM_STREAM"]
    status["run"] = pl.pl1000Run(chandle, circularBufferSamples, mode)
    assert_pico_ok(status["run"])

    sleep(usForBlock.value / 1000000)

    values = (ctypes.c_uint16 * requestedSamples)()
    overflow = ctypes.c_uint16()
    triggerIndex = ctypes.c_uint32()

    # noOfValues is an in/out argument: it goes in as the buffer capacity and
    # comes back as the number of samples the driver actually returned, so it is
    # kept separate from requestedSamples rather than reusing one variable for
    # both. triggerIndex is passed as a real pointer rather than None, so the
    # driver always has somewhere to write it.
    noOfValues = ctypes.c_uint32(requestedSamples)

    status["getValues"] = pl.pl1000GetValues(chandle, ctypes.byref(values), ctypes.byref(noOfValues), ctypes.byref(overflow), ctypes.byref(triggerIndex))
    assert_pico_ok(status["getValues"])

    samplesCollected = min(noOfValues.value, requestedSamples)
    print(f"{samplesCollected} samples collected")

    if overflow.value:
        print("Warning: the channel went over range during this capture.")

    # convert ADC counts data to mV
    maxADC = ctypes.c_uint16()
    status["maxValue"] = pl.pl1000MaxValue(chandle, ctypes.byref(maxADC))
    assert_pico_ok(status["maxValue"])

    # Only the samples the driver actually returned are converted; the rest of
    # the buffer is still zero and is not data.
    mVValues = adc2mVpl1000(values[:samplesCollected], pl.PL1000_FULL_SCALE_MV, maxADC)

    # create time data
    # The sample interval comes from the block length and the number of samples
    # requested for it, not from the count that came back.
    interval = (0.001 * usForBlock.value) / requestedSamples

    timeMs = np.linspace(0, (len(mVValues) - 1) * interval, len(mVValues))

finally:
    # stop the device before closing it, so it is not left converting
    status["stop"] = pl.pl1000Stop(chandle)
    assert_pico_ok(status["stop"])

    # close PicoLog 1000 device
    status["closeUnit"] = pl.pl1000CloseUnit(chandle)
    assert_pico_ok(status["closeUnit"])

# plot data
plt.plot(timeMs, mVValues)
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
plt.show()

# display status returns
print(status)
