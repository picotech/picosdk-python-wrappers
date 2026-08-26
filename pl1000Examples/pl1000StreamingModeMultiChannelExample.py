#
# Copyright (C) 2025 Pico Technology Ltd. See LICENSE file for terms.
#
# PL1000 STREAMING MODE MULTICHANNEL EXAMPLE
# This example opens a PicoLog 1000 device, configures streaming mode to capture data from N channels
# at the set sample rate, retrieves the data, and displays it on a plot.

import ctypes
import time

import numpy
from picosdk.pl1000 import pl1000 as pl
import matplotlib.pyplot as plt
from picosdk.functions import assert_pico_ok, adc2mVpl1000

# Setup channels values and arrays
channel_list=(1,2,3,4,5,6,7,8,9,10,11,12) # Enable Chs 1-12, Max channels (1012)
# channel_list=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16) # Enable Chs 1-16, Max channels (1216)
n_channels = len(channel_list)
print(f"{n_channels} channels")
channel_array = (ctypes.c_int16 * len(channel_list))()
for i, ch in enumerate(channel_list):
    channel_array[i] = pl.PL1000Inputs[f"PL1000_CHANNEL_{ch}"]

# Max streaming sample rate for
# 1012 - with all 12 channels on is = 100k /12 = 8333S/s
# 1216 - with all 16 channels on is = 100k /16 = 6250S/s
us_for_block = ctypes.c_uint32(1_000_000)   # 1 seconds in microseconds
ideal_no_of_samples = 6250                  # Max sample rate for both 1012/1216 with 12 Chs on

# As us_for_block is set to 1M, "ideal_no_of_samples" becomes the sample rate per channel (in Samples/second)
read_buffer_size = ideal_no_of_samples * n_channels

# Number of download iterations, and how long to let the buffer fill between them
n_iterations = 9
seconds_between_reads = 0.1

# reserve memory
read_buffer = (ctypes.c_uint16 * read_buffer_size)() # reserve memory for read_buffer
captured_samples=numpy.zeros(shape=(0,n_channels), dtype=numpy.uint16)

# Datatypes for Addition capture Info
overflow = ctypes.c_uint16()
triggerIndex = ctypes.c_uint32()
overflow_seen = 0

# Open the device
handle = ctypes.c_int16()
assert_pico_ok(pl.pl1000OpenUnit(ctypes.byref(handle)))

# Everything after the unit is open runs inside try/finally so the unit is
# always stopped and released, including when a call fails and assert_pico_ok
# raises. Without this a failure part-way through left the device streaming.
try:
    # Configure sampling interval
    assert_pico_ok(
        pl.pl1000SetInterval(
            handle,
            ctypes.byref(us_for_block),
            ctypes.c_uint32(ideal_no_of_samples),
            channel_array,
            len(channel_list)
        )
    )

    print(f'ideal_no_of_samples: {ideal_no_of_samples}')
    print(f'read_buffer_size: {read_buffer_size}')
    print(f'us_for_block: {us_for_block.value} us')

    # start acquisition
    # In BM_STREAM mode this count is the size of the driver's circular buffer,
    # in samples per channel. It holds one second of data here, and the loop
    # below reads every 0.1 s, so it never fills.
    assert_pico_ok(
        pl.pl1000Run(
            handle,
            ctypes.c_uint32(read_buffer_size),
            pl.PL1000_BLOCK_METHOD["BM_STREAM"]
            )
        )

    # Check device is ready using IsReady
    ready = ctypes.c_int16(0)
    while ready.value == 0:
        assert_pico_ok(
            pl.pl1000Ready(handle, ctypes.byref(ready))
            )

        # Yield between polls rather than spinning on the driver as fast as the
        # interpreter can call it.
        time.sleep(0.01)

    # start download loop:
    for iteration_idx in range(n_iterations):
        time.sleep(seconds_between_reads) # wait to part fill the buffer (never let it fill up!!)

        # In/out argument: goes in as the per-channel capacity of read_buffer and
        # comes back as the number of samples per channel actually returned.
        read_sample_count = ctypes.c_uint32(read_buffer_size // n_channels)

        assert_pico_ok(
            pl.pl1000GetValues(
                handle,
                ctypes.byref(read_buffer),
                ctypes.byref(read_sample_count),    # gets modified on return (per channel)
                ctypes.byref(overflow),             # Channel voltage over range bit flags (LSB is Ch0)
                ctypes.byref(triggerIndex)
            )
        )
        # check how many samples have actually been captured:

        # Never read past the end of read_buffer, whatever the driver reports.
        samples_this_read = min(read_sample_count.value, read_buffer_size // n_channels)

        overflow_seen |= overflow.value

        print(f"iteration {iteration_idx}: readout {samples_this_read} samples across {n_channels} channels")

        read_samples_numpy_varsized = numpy.array(read_buffer[:samples_this_read * n_channels]) # get only the valid samples out of the read_buffer
        print(f'  - read_samples_numpy_varsized.shape: {read_samples_numpy_varsized.shape}')

        # now, we can reshape the running buffer, which is now well sized, to a 2D array:
        channelized_samples = read_samples_numpy_varsized.reshape((-1,n_channels))
        # Append to final Array
        captured_samples = numpy.vstack((captured_samples,channelized_samples))

        # Debug - list array sizes
        # print(f'  - channelized_samples.shape: {channelized_samples.shape}')
        # print(f'  - captured_samples.shape: {captured_samples.shape}')
        # print('---')

    # Read the maximum ADC count so the readings can be scaled to millivolts
    maxADC = ctypes.c_uint16()
    assert_pico_ok(pl.pl1000MaxValue(handle, ctypes.byref(maxADC)))

finally:
    # Stop the device before closing it, so it is not left converting
    assert_pico_ok(pl.pl1000Stop(handle))

    # Close unit
    assert_pico_ok(pl.pl1000CloseUnit(handle))

# Display data
print(f'Final captured_samples (Samples, NoOfChannels): {captured_samples.shape}')
print(f'Channel_list: {channel_list}')

if overflow_seen:
    # The flags are per channel, least significant bit first.
    over_range = [channel_list[i] for i in range(n_channels) if overflow_seen & (1 << i)]
    print(f'Warning: channels over range during this capture: {over_range}')

# ideal_no_of_samples samples per channel are taken over us_for_block
# microseconds, so the rate is samples divided by the block length in seconds.
samples_per_s = ideal_no_of_samples / (us_for_block.value / 1_000_000)
interval = 1 / samples_per_s
print(f" { interval }s Sample Interval = { samples_per_s }Samples/sec ")

time_s = numpy.linspace(0, (len(captured_samples[:,0]) -1) * interval, len(captured_samples[:,0]))

# Plot every enabled channel, driven by channel_list rather than one hard-coded
# line per channel: those had to be edited by hand whenever the channel count
# changed, and indexed past the end of the array if it was reduced.
for i, ch in enumerate(channel_list):
    if maxADC.value > 0:
        plt.plot(time_s, adc2mVpl1000(captured_samples[:, i], pl.PL1000_FULL_SCALE_MV, maxADC), label=f'Ch{ch}')
    else:
        plt.plot(time_s, captured_samples[:, i], label=f'Ch{ch}')

plt.xlabel('Time (s)')
plt.ylabel('Voltage (mV)' if maxADC.value > 0 else 'ADC counts')
plt.legend(ncol=2, fontsize='small')
plt.show()
