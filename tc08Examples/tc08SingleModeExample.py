#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# TC-08 SINGLE MODE EXAMPLE


import ctypes
import numpy as np
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open unit
status["open_unit"] = tc08.usb_tc08_open_unit()
assert_pico2000_ok(status["open_unit"])
chandle = status["open_unit"]

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
status["get_minimum_interval_ms"] = tc08.usb_tc08_get_minimum_interval_ms(chandle)
assert_pico2000_ok(status["get_minimum_interval_ms"])

# get single temperature reading
temp = (ctypes.c_float * 9)()
overflow = ctypes.c_int16(0)
units = tc08.USBTC08_UNITS["USBTC08_UNITS_CENTIGRADE"]
status["get_single"] = tc08.usb_tc08_get_single(chandle,ctypes.byref(temp), ctypes.byref(overflow), units)
assert_pico2000_ok(status["get_single"])

# print data
print("Cold Junction ", temp[0]," Channel 1 ", temp[1])


# close unit
status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
assert_pico2000_ok(status["close_unit"])

# display status returns
print(status)