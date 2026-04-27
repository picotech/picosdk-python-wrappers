#
# Copyright (C) 2026 Pico Technology Ltd. See LICENSE file for terms.
#
# TC-08 STREAMING MODE EXAMPLE

import ctypes
import time
import numpy as np
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

# --- Configuration ---
NUM_SAMPLES = 100
Requested_No_Samples = 5 # per function call - sets the loop delay (min. value is 1)
# Define which channels to enable (1-8). 0 is the Cold Junction.
ENABLED_CHANNELS = [1, 2, 8] 
THERMOCOUPLE_TYPE = ord('K') # 'K' type. Use 32 (ASCII space) to disable.
# ---------------------

# Create status dictionary to track API calls
status = {}

# Open Unit
status["open_unit"] = tc08.usb_tc08_open_unit()
assert_pico2000_ok(status["open_unit"])
chandle = status["open_unit"]

try:
    # Set Mains Rejection (50Hz = 0, 60Hz = 1)
    status["set_mains"] = tc08.usb_tc08_set_mains(chandle, 0)
    assert_pico2000_ok(status["set_mains"])

    # Setup Channels
    # Always set channel 0 (Cold Junction)
    #tc08.usb_tc08_set_channel(chandle, 0, ord(' ')) 
    Enabled_chs = 0
    for chan in ENABLED_CHANNELS:
        status[f"set_chan_{chan}"] = tc08.usb_tc08_set_channel(chandle, chan, THERMOCOUPLE_TYPE)
        assert_pico2000_ok(status[f"set_chan_{chan}"])
        Enabled_chs = Enabled_chs + 1

    # Get the minimum sampling interval
    # This determines how fast the device can switch between enabled channels
    min_interval_ms = tc08.usb_tc08_get_minimum_interval_ms(chandle)
    status["get_temp_return"] = min_interval_ms
    assert_pico2000_ok(status["get_temp_return"])
    print(f"Minimum sampling interval: {min_interval_ms} ms")

    # Prepare Data Storage
    # We need a buffer for each channel's samples
    # data_store[channel_index][sample_index]
    #captured_samples=np.zeros(shape=(9, NUM_SAMPLES), dtype=ctypes.c_float)
    rows, cols = 9, NUM_SAMPLES
    RowType = ctypes.c_float * cols
    Array2D = RowType * rows
    captured_samples = Array2D()
    
    # Buffers required by usb_tc08_get_temp
    # It returns up to 'buffer_length' samples per call
    temp_buffer = (ctypes.c_float * 600)() # Buffer
    times_ms_buffer = (ctypes.c_int32 * 600)() 
    overflow = ctypes.c_int16()

    # set tc-08 running
    status["run"] = tc08.usb_tc08_run(chandle, min_interval_ms)
    assert_pico2000_ok(status["run"])

    print(f"Starting capture of {NUM_SAMPLES} samples...")
    current_num_samples = 0
    # Collection Loop
    while current_num_samples in range(NUM_SAMPLES):
        # We call get_temp for each sample point
        # The library fills the buffer with the most recent readings
        # Store the data for our enabled channels
        for chan in ENABLED_CHANNELS:
            get_temp_return = tc08.usb_tc08_get_temp(
                chandle, 
                ctypes.byref(temp_buffer), 
                ctypes.byref(times_ms_buffer), 
                len(temp_buffer),
                ctypes.byref(overflow), # Chanel over range flag
                chan, # channel
                0, # units (0 = Centigrade)
                1  # fill_missing samples
            )
            if(get_temp_return < 0):
                status["get_temp_return"] = get_temp_return
                assert_pico2000_ok(status["get_temp_return"])
            
            if(get_temp_return > 0): # If Samples
                if((current_num_samples+get_temp_return) < NUM_SAMPLES): 
                    captured_samples[chan][current_num_samples:(current_num_samples+get_temp_return)] = temp_buffer[0:get_temp_return]

        current_num_samples = current_num_samples + get_temp_return

        # Print current values from channels-
        if(get_temp_return > 0):
            for chan in ENABLED_CHANNELS:
                print("Channel: ", chan )
                print("Channel Temps: ", captured_samples[chan][current_num_samples-get_temp_return])

        # Delay by the minimum interval to ensure hardware is ready for next conversion
        time.sleep(min_interval_ms * Requested_No_Samples / 1000.0)

        if current_num_samples % 10 == 0:
            print(f"Captured {current_num_samples} samples...")

    print("Capture complete.")

finally:
    # Close Unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    print("Device closed.")