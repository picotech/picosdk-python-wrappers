#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# PICOHRDL SINGLE MODE EXAMPLE


import ctypes
import numpy as np
from picosdk.picohrdl import picohrdl as hrdl
from picosdk.functions import assert_pico2000_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open unit
status["openUnit"] = hrdl.HRDLOpenUnit()
assert_pico2000_ok(status["openUnit"])
chandle=status["openUnit"]

# set mains noise rejection
# reject 50 Hz mains noise
status["mainsRejection"] = hrdl.HRDLSetMains(chandle, 0)
assert_pico2000_ok(status["mainsRejection"])

# set single reading
range = hrdl.HRDL_VOLTAGERANGE["HRDL_2500_MV"]
conversionTime = hrdl.HRDL_CONVERSIONTIME["HRDL_100MS"]
overflow = ctypes.c_int16(0)
value = ctypes.c_int32()
status["getSingleValue"] = hrdl.HRDLGetSingleValue(chandle, 5, range, conversionTime, 1, ctypes.byref(overflow), ctypes.byref(value))
assert_pico2000_ok(status["getSingleValue"])

# display value
print(value.value)

# close unit
status["closeUnit"] = hrdl.HRDLCloseUnit(chandle)
assert_pico2000_ok(status["closeUnit"])

# print status
print(status)