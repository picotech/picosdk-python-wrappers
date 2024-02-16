#
# Copyright (C) 2024 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 A GET UNIT INFO EXAMPLE
# This example opens a 6000a driver device, collects the model and serial nubmber from the device and closes the device.

import ctypes
import numpy as np
from picosdk.ps6000a import ps6000a as ps
from picosdk.PicoDeviceEnums import picoEnum as enums
from picosdk.functions import assert_pico_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 6000 A series PicoScope
# returns handle to chandle for use in future API functions
resolution = enums.PICO_DEVICE_RESOLUTION["PICO_DR_8BIT"]
status["openunit"] = ps.ps6000aOpenUnit(ctypes.byref(chandle), None, resolution)
assert_pico_ok(status["openunit"])

# Get unit info
modelNum = ctypes.create_string_buffer(6)
modelNumString = ctypes.cast(modelNum,ctypes.c_char_p)
stringLength = len(modelNum)
requiredSize = ctypes.c_int16(stringLength)
infoModel= 0x03
status["getUnitInfo_Model"] = ps.ps6000aGetUnitInfo(chandle, modelNumString,stringLength,ctypes.byref(requiredSize),infoModel)
assert_pico_ok(status["getUnitInfo_Model"])
print(modelNum.value)

SN = ctypes.create_string_buffer(b"AA000/0000")
SNString = ctypes.cast(SN,ctypes.c_char_p)
stringLength = len(SN)
requiredSize = ctypes.c_int16(stringLength)
infoSN = 0x04
status["getUnitInfo_SN"] = ps.ps6000aGetUnitInfo(chandle, SNString,stringLength,ctypes.byref(requiredSize),infoSN)
assert_pico_ok(status["getUnitInfo_SN"])
print(SN.value)

# Close the scope
status["closeunit"] = ps.ps6000aCloseUnit(chandle)
assert_pico_ok(status["closeunit"])


print(status)