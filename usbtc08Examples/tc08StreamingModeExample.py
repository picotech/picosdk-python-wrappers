#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# TC-08 STREAMING MODE EXAMPLE


import ctypes
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
import matplotlib.pyplot as plt

# Number of readings to ask the driver for. usb_tc08_get_temp never returns
# more than USBTC08_MAX_SAMPLE_BUFFER readings in one call.
NUM_SAMPLES = 100

# Create status ready for use
status = {}

# open unit
# usb_tc08_open_unit returns a positive handle, 0 if no unit was found, or a
# negative value on error, so it doubles as the status for this call.
status["open_unit"] = tc08.usb_tc08_open_unit()
assert_pico2000_ok(status["open_unit"])
chandle = status["open_unit"]

# Everything after the unit is open runs inside try/finally so the unit is
# always stopped and released, including when a call fails and
# assert_pico2000_ok raises. Without this a failure part-way through left the
# device streaming.
try:
    # set mains rejection to 50 Hz
    status["set_mains"] = tc08.usb_tc08_set_mains(chandle,0)
    assert_pico2000_ok(status["set_mains"])

    # set up channel
    # therocouples types and int8 equivalent
    # B=66 , E=69 , J=74 , K=75 , N=78 , R=82 , S=83 , T=84 , ' '=32 , X=88
    typeK = ctypes.c_int8(75)
    status["set_channel"] = tc08.usb_tc08_set_channel(chandle, 1, typeK)
    assert_pico2000_ok(status["set_channel"])

    # get minimum sampling interval in ms
    # This returns the interval itself rather than a status code, so it is
    # checked directly: a value of zero or less means the call failed.
    minimum_interval_ms = tc08.usb_tc08_get_minimum_interval_ms(chandle)
    status["get_minimum_interval_ms"] = minimum_interval_ms

    if minimum_interval_ms <= 0:
        raise RuntimeError("usb_tc08_get_minimum_interval_ms failed: %d" % minimum_interval_ms)

    # set tc-08 running
    # usb_tc08_run returns the interval the driver actually applied, or 0 if
    # streaming could not be started.
    status["run"] = tc08.usb_tc08_run(chandle, minimum_interval_ms)
    assert_pico2000_ok(status["run"])
    actual_interval_ms = status["run"]

    # Wait long enough for the requested number of readings to be converted,
    # rather than for a fixed number of seconds that has to be kept in step
    # with NUM_SAMPLES by hand. usb_tc08_get_temp must be called at least once
    # a minute or readings are lost, so the wait is capped below that.
    collection_time_s = min(NUM_SAMPLES * actual_interval_ms / 1000.0, 50.0)
    print("Collecting for %.1f s at %d ms per reading..." % (collection_time_s, actual_interval_ms))
    time.sleep(collection_time_s)

    # collect data
    # One float and one time per reading. The previous (c_float * 2 * 100)
    # allocated 100 pairs of floats, which does not match what the driver
    # writes and made the plot below show two series instead of one.
    temp_buffer = (ctypes.c_float * NUM_SAMPLES)()
    times_ms_buffer = (ctypes.c_int32 * NUM_SAMPLES)()
    overflow = ctypes.c_int16()
    units = tc08.USBTC08_UNITS["USBTC08_UNITS_CENTIGRADE"]
    status["get_temp"] = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer), ctypes.byref(times_ms_buffer), NUM_SAMPLES, ctypes.byref(overflow), 1, units, 1)
    assert_pico2000_ok(status["get_temp"])
    samples = status["get_temp"]

    if overflow.value:
        print("Warning: channel 1 was over range during this capture.")

finally:
    # stop unit
    status["stop"] = tc08.usb_tc08_stop(chandle)
    assert_pico2000_ok(status["stop"])

    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])

# plot data
# usb_tc08_get_temp reports times in milliseconds, not nanoseconds.
plt.plot(times_ms_buffer[0:samples], temp_buffer[0:samples])
plt.xlabel('Time (ms)')
plt.ylabel('Temperature (oC)')
plt.show()

# display status returns
print(status)
