#
# Copyright (C) 2025 Pico Technology Ltd. See LICENSE file for terms.
#
# PL1000 STREAMING MODE MULTICHANNEL EXAMPLE
# This example opens a PicoLog 1000 device, configures streaming mode to capture data from N channels
# at the set sample rate, retrieves the data, and displays it on a plot.

import ctypes
import time
from typing import Optional

import numpy
import picosdk.pl1000
import matplotlib.pyplot as plt
from picosdk.functions import assert_pico_ok, adc2mVpl1000

# Setup channels values and arrays
channel_list=(1,2,3,4,5,6,7,8,9,10,11,12) # Enable Chs 1-12, Max channels (1012)
# channel_list=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16) # Enable Chs 1-16, Max channels (1216)
n_channels = len(channel_list)
print(f"{n_channels} channels")
channel_array = (ctypes.c_int16 * len(channel_list))()
for i, ch in enumerate(channel_list):
    channel_array[i] = picosdk.pl1000.pl1000.PL1000Inputs[f"PL1000_CHANNEL_{ch}"]  

# Max streaming sample rate for
# 1012 - with all 12 channels on is = 100k /12 = 8333S/s
# 1216 - with all 16 channels on is = 100k /16 = 6250S/s
us_for_block = ctypes.c_uint32(1_000_000)   # 1 seconds in microseconds              
ideal_no_of_samples = 6250                  # Max sample rate for both 1012/1216 with 12 Chs on

# As us_for_block is set to 1M, "ideal_no_of_samples" becomes the sample rate per channel (in Samples/second)       
read_buffer_size = ideal_no_of_samples * n_channels
read_sample_count = ctypes.c_uint32(read_buffer_size)      

# reserve memory    
read_buffer = (ctypes.c_uint16 * read_buffer_size)() # reserve memory for read_buffer
captured_samples=numpy.zeros(shape=(0,n_channels), dtype=numpy.uint16)
leftover_sample_buffer = numpy.zeros(shape=(0,), dtype=numpy.uint16)
leftover_sample_counter = 0

# Datatypes for Addition capture Info
overflow = ctypes.c_uint16()
triggerIndex = ctypes.c_uint32()

# Open the device
handle = ctypes.c_int16()
assert_pico_ok(picosdk.pl1000.pl1000.pl1000OpenUnit(ctypes.byref(handle)))

# Configure sampling interval
assert_pico_ok(
    picosdk.pl1000.pl1000.pl1000SetInterval(
        handle,
        ctypes.byref(us_for_block),
        ctypes.c_uint32(ideal_no_of_samples),
        channel_array,
        len(channel_list)
    )
)

print(f'ideal_no_of_samples: {ideal_no_of_samples}')
print(f'read_buffer_size: {read_buffer_size}')
print(f'us_for_block: {us_for_block}')

# start acquisition
assert_pico_ok(
    picosdk.pl1000.pl1000.pl1000Run(
        handle,
        ctypes.c_uint32(read_buffer_size),
        picosdk.pl1000.pl1000.PL1000_BLOCK_METHOD["BM_STREAM"]
        )
    )

# Check device is ready using IsReady
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    assert_pico_ok(
        picosdk.pl1000.pl1000.pl1000Ready(handle, ctypes.byref(ready))
        )

# start download loop:
for iteration_idx in range(9):
    time.sleep(0.1) # wait to part fill the buffer (never let it fill up!!)

    read_sample_count = ctypes.c_uint32((int)(read_buffer_size // n_channels))

    assert_pico_ok(
        picosdk.pl1000.pl1000.pl1000GetValues(
            handle,
            ctypes.byref(read_buffer),
            ctypes.byref(read_sample_count),    # gets modified on return (per channel)
            ctypes.byref(overflow),             # Channel voltage over range bit flags (LSB is Ch0)
            ctypes.byref(triggerIndex)
        )
    )
    # check how many samples have actually been captured:

    print(f"iteration {iteration_idx}: readout {read_sample_count.value} samples across {n_channels} channels")

    read_samples_numpy_varsized = numpy.array(read_buffer[:read_sample_count.value * n_channels]) # get only the valid samples out of the read_buffer
    print(f'  - read_samples_numpy_varsized.shape: {read_samples_numpy_varsized.shape}')

    # now, we can reshape the running buffer, which is now well sized, to a 2D array:
    channelized_samples = read_samples_numpy_varsized.reshape((-1,n_channels))
    # Append to final Array
    captured_samples = numpy.vstack((captured_samples,channelized_samples))

    # Debug - list array sizes
    # print(f'  - channelized_samples.shape: {channelized_samples.shape}')
    # print(f'  - captured_samples.shape: {captured_samples.shape}')
    # print('---')

# Close unit                           
assert_pico_ok(picosdk.pl1000.pl1000.pl1000CloseUnit(handle))        

# Display data
print(f'Final captured_samples (Samples, NoOfChannels): {captured_samples.shape}')
print(f'Channel_list: {channel_list}')
samples_per_s = (ideal_no_of_samples * us_for_block.value / 1_000_000)
interval = 1 / samples_per_s
print(f" { interval }s Sample Interval = { samples_per_s }Samples/sec ")

time_s = numpy.linspace(0, (len(captured_samples[:,0]) -1) * interval, len(captured_samples[:,0]))
plt.plot(time_s, captured_samples[:,0])
plt.plot(time_s, captured_samples[:,1])
plt.plot(time_s, captured_samples[:,2]) # 3 channels
plt.plot(time_s, captured_samples[:,3])
plt.plot(time_s, captured_samples[:,4])
plt.plot(time_s, captured_samples[:,5]) # 6 channels
plt.plot(time_s, captured_samples[:,6])
plt.plot(time_s, captured_samples[:,7])
plt.plot(time_s, captured_samples[:,8]) # 9 channels
plt.plot(time_s, captured_samples[:,9])
plt.plot(time_s, captured_samples[:,10])
plt.plot(time_s, captured_samples[:,11]) # 12 Max channels (1012)
#plt.plot(time_s, captured_samples[:,12])
#plt.plot(time_s, captured_samples[:,13])
#plt.plot(time_s, captured_samples[:,14])
#plt.plot(time_s, captured_samples[:,15]) # 16 Max channels (1216)

plt.xlabel('Time (s)')
plt.ylabel('ADC counts')
plt.show()