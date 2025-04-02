#
# Copyright (C) 2025 Pico Technology Ltd. See LICENSE file for terms.
#
# PT104 Example
# This example opens a pt104, sets up a single channel and collects data before closing the pt104

import ctypes
from picosdk.usbPT104 import usbPt104 as pt104
import numpy as np
from picosdk.functions import assert_pico_ok
from time import sleep
import matplotlib.pyplot as plt

# Create status ready for use
status = {}

# Setup Enumerating function data types
Enumerate_string = ctypes.create_string_buffer(b"------------------------------------------------------------------")
EnumUnitString = ctypes.cast(Enumerate_string,ctypes.c_char_p)
stringLength = len(Enumerate_string)
requiredSize = ctypes.c_uint32(stringLength)

unit_connection_method = pt104.COMMUNICATION_TYPE["CT_USB"]

print("Enumerating Unit(s)...")
status["EnumerateUnit"] = pt104.UsbPt104Enumerate(EnumUnitString, ctypes.byref(requiredSize) , unit_connection_method )
assert_pico_ok(status["EnumerateUnit"])
print("serial number(s) are-")
print(EnumUnitString.value)

# Create variables for unit handles
chandle = ctypes.c_int16()
chandle2 = ctypes.c_int16()

# Open the device
print("Opening device...")
status["openUnit"] = pt104.UsbPt104OpenUnit(ctypes.byref(chandle),0)
assert_pico_ok(status["openUnit"])
print("handle is: ", chandle)

SN = ctypes.create_string_buffer(b"AA000/0000")
SNString = ctypes.cast(SN,ctypes.c_char_p)
stringLength = len(SN)
requiredSize = ctypes.c_int16(stringLength)
infoSN = 0x04

status["getUnitInfo_SN"] = pt104.UsbPt104GetUnitInfo(chandle, SNString,stringLength,ctypes.byref(requiredSize),infoSN)
assert_pico_ok(status["getUnitInfo_SN"])
print("Serial number is...")
print(SN.value)

# Open the 2nd device
print("Opening the 2nd device...")
status["openUnit"] = pt104.UsbPt104OpenUnit(ctypes.byref(chandle2),0)
assert_pico_ok(status["openUnit"])
print("handle is: ", chandle2)

status["getUnitInfo_SN"] = pt104.UsbPt104GetUnitInfo(chandle2, SNString,stringLength,ctypes.byref(requiredSize),infoSN)
assert_pico_ok(status["getUnitInfo_SN"])
print("Serial number is...")
print(SN.value)

# Close the unit(s)
print("Closing Unit(s)...")
status["closeUnit"] = pt104.UsbPt104CloseUnit(chandle)
assert_pico_ok(status["closeUnit"])
status["closeUnit"] = pt104.UsbPt104CloseUnit(chandle2)
assert_pico_ok(status["closeUnit"])

print(status)
