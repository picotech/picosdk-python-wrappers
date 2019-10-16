#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# PICOLOG HIGH RESOLUTION DATA LOGGER SINGLE MODE EXAMPLE
#
# This example demonstrates how to capture a single value from an ADC-20 or ADC-24 Precision Data Loggers.


import ctypes
import numpy as np
from picosdk.picohrdl import picohrdl as hrdl
from picosdk.functions import assert_pico2000_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open unit
status["openUnit"] = hrdl.HRDLOpenUnit()
assert_pico2000_ok(status["openUnit"])
chandle=status["openUnit"]

# Set mains noise rejection
# Reject 50 Hz mains noise
status["mainsRejection"] = hrdl.HRDLSetMains(chandle, 0)
assert_pico2000_ok(status["mainsRejection"])

# Set single reading
range = hrdl.HRDL_VOLTAGERANGE["HRDL_2500_MV"]
conversionTime = hrdl.HRDL_CONVERSIONTIME["HRDL_100MS"]
overflow = ctypes.c_int16(0)
value = ctypes.c_int32()
status["getSingleValue"] = hrdl.HRDLGetSingleValue(chandle, 5, range, conversionTime, 1, ctypes.byref(overflow), ctypes.byref(value))
assert_pico2000_ok(status["getSingleValue"])

# Display value
print(value.value)

# Close unit
status["closeUnit"] = hrdl.HRDLCloseUnit(chandle)
assert_pico2000_ok(status["closeUnit"])

# Print status
print(status)