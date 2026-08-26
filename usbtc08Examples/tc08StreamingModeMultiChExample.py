#
# Copyright (C) 2026 Pico Technology Ltd. See LICENSE file for terms.
#
# TC-08 STREAMING MODE EXAMPLE

import ctypes
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

# --- Configuration ---
NUM_SAMPLES = 100
REQUESTED_NO_SAMPLES = 5 # per function call - sets the loop delay (min. value is 1)
# Define which channels to enable (1-8). 0 is the Cold Junction.
ENABLED_CHANNELS = [1, 2, 8]
THERMOCOUPLE_TYPE = ord('K') # 'K' type. Use 32 (ASCII space) to disable.
# Give up if the driver returns no readings for this many consecutive passes,
# so a device that stops delivering data cannot spin this loop forever.
MAX_EMPTY_PASSES = 20
# ---------------------

if not ENABLED_CHANNELS:
    raise ValueError("ENABLED_CHANNELS must list at least one channel")

if any(chan < 1 or chan > tc08.USBTC08_MAX_CHANNELS for chan in ENABLED_CHANNELS):
    raise ValueError("ENABLED_CHANNELS must contain channels 1 to %d" % tc08.USBTC08_MAX_CHANNELS)

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
    # Channel 0 (the Cold Junction) does not need to be set up to read the
    # thermocouple inputs, so it is left alone here.
    for chan in ENABLED_CHANNELS:
        status[f"set_chan_{chan}"] = tc08.usb_tc08_set_channel(chandle, chan, THERMOCOUPLE_TYPE)
        assert_pico2000_ok(status[f"set_chan_{chan}"])

    # Get the minimum sampling interval
    # This determines how fast the device can switch between enabled channels.
    # It returns the interval itself rather than a status code, so it is checked
    # directly: a value of zero or less means the call failed.
    min_interval_ms = tc08.usb_tc08_get_minimum_interval_ms(chandle)
    status["get_minimum_interval_ms"] = min_interval_ms

    if min_interval_ms <= 0:
        raise RuntimeError("usb_tc08_get_minimum_interval_ms failed: %d" % min_interval_ms)

    print(f"Minimum sampling interval: {min_interval_ms} ms")

    # Prepare Data Storage
    # We need a buffer for each channel's samples
    # captured_samples[channel_index][sample_index]
    rows, cols = tc08.USBTC08_MAX_CHANNELS + 1, NUM_SAMPLES
    RowType = ctypes.c_float * cols
    Array2D = RowType * rows
    captured_samples = Array2D()

    # Buffers required by usb_tc08_get_temp. It returns up to 'buffer_length'
    # samples per call, and never more than USBTC08_MAX_SAMPLE_BUFFER.
    temp_buffer = (ctypes.c_float * tc08.USBTC08_MAX_SAMPLE_BUFFER)()
    times_ms_buffer = (ctypes.c_int32 * tc08.USBTC08_MAX_SAMPLE_BUFFER)()
    overflow = ctypes.c_int16()
    units = tc08.USBTC08_UNITS["USBTC08_UNITS_CENTIGRADE"]

    # set tc-08 running
    # usb_tc08_run returns the interval the driver actually applied, or 0 if
    # streaming could not be started.
    status["run"] = tc08.usb_tc08_run(chandle, min_interval_ms)
    assert_pico2000_ok(status["run"])

    print(f"Starting capture of {NUM_SAMPLES} samples...")
    current_num_samples = 0
    empty_passes = 0

    # Collection Loop
    while current_num_samples < NUM_SAMPLES:
        # Only advance by the number of readings every enabled channel
        # returned. The driver reports a count per channel and those counts can
        # differ, so tracking the smallest keeps the channels aligned in
        # captured_samples.
        samples_this_pass = None

        # Never write past the end of captured_samples.
        room_left = NUM_SAMPLES - current_num_samples

        for chan in ENABLED_CHANNELS:
            get_temp_return = tc08.usb_tc08_get_temp(
                chandle,
                ctypes.byref(temp_buffer),
                ctypes.byref(times_ms_buffer),
                len(temp_buffer),
                ctypes.byref(overflow), # Chanel over range flag
                chan, # channel
                units,
                1  # fill_missing samples
            )

            if get_temp_return < 0:
                status["get_temp_return"] = get_temp_return
                assert_pico2000_ok(status["get_temp_return"])

            # Store what fits. The previous version discarded the whole block
            # whenever it would have crossed NUM_SAMPLES, so the tail of the
            # capture was always left as zeros.
            to_store = min(get_temp_return, room_left)

            if to_store > 0:
                captured_samples[chan][current_num_samples:(current_num_samples + to_store)] = \
                    temp_buffer[0:to_store]

            if samples_this_pass is None or to_store < samples_this_pass:
                samples_this_pass = to_store

        if samples_this_pass:
            empty_passes = 0

            # Print current values from channels-
            for chan in ENABLED_CHANNELS:
                print("Channel: ", chan)
                print("Channel Temps: ", captured_samples[chan][current_num_samples])

            current_num_samples = current_num_samples + samples_this_pass
            print(f"Captured {current_num_samples} samples...")
        else:
            empty_passes = empty_passes + 1

            if empty_passes >= MAX_EMPTY_PASSES:
                raise RuntimeError(
                    "No readings returned in %d consecutive passes; giving up." % empty_passes)

        # Delay by the minimum interval to ensure hardware is ready for next conversion
        time.sleep(min_interval_ms * REQUESTED_NO_SAMPLES / 1000.0)

    print("Capture complete.")

finally:
    # Stop the unit before closing it, so it is not left converting.
    status["stop"] = tc08.usb_tc08_stop(chandle)
    assert_pico2000_ok(status["stop"])

    # Close Unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    print("Device closed.")
