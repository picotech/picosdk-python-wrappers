#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# TC-08 SINGLE MODE EXAMPLE


import ctypes
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

# Create status ready for use
status = {}

# open unit
# usb_tc08_open_unit returns a positive handle, 0 if no unit was found, or a
# negative value on error, so it doubles as the status for this call.
status["open_unit"] = tc08.usb_tc08_open_unit()
assert_pico2000_ok(status["open_unit"])
chandle = status["open_unit"]

# Everything after the unit is open runs inside try/finally so the unit is
# always released, including when a call fails and assert_pico2000_ok raises.
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

    print("Minimum sampling interval:", minimum_interval_ms, "ms")

    # get single temperature reading
    # The driver fills one entry per channel: the cold junction plus the eight
    # thermocouple inputs.
    temp = (ctypes.c_float * (tc08.USBTC08_MAX_CHANNELS + 1))()
    overflow = ctypes.c_int16(0)
    units = tc08.USBTC08_UNITS["USBTC08_UNITS_CENTIGRADE"]
    status["get_single"] = tc08.usb_tc08_get_single(chandle,ctypes.byref(temp), ctypes.byref(overflow), units)
    assert_pico2000_ok(status["get_single"])

    # print data
    print("Cold Junction ", temp[0]," Channel 1 ", temp[1])

finally:
    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])

# display status returns
print(status)
