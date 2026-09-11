#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# PL1000 SINGLE MODE EXAMPLE
# This example opens a pl1000 device, sets up the device for capturing data from channel 1.
# Then this example collect a sample from channel 1 and displays it on the console.

import ctypes
from picosdk.pl1000 import pl1000 as pl
from picosdk.functions import assert_pico_ok

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open PicoLog 1000 device
status["openUnit"] = pl.pl1000OpenUnit(ctypes.byref(chandle))
assert_pico_ok(status["openUnit"])

# Everything after the unit is open runs inside try/finally so the unit is
# always released, including when a call fails and assert_pico_ok raises.
try:
    # get the maximum ADC count, needed to scale the reading to millivolts
    maxADC = ctypes.c_uint16()
    status["maxValue"] = pl.pl1000MaxValue(chandle, ctypes.byref(maxADC))
    assert_pico_ok(status["maxValue"])

    # pl1000GetSingle writes a uint16_t, so the buffer must be c_uint16
    value = ctypes.c_uint16()
    # get a single ADC count value from channel 1
    status["getSingle"] = pl.pl1000GetSingle(chandle, pl.PL1000Inputs["PL1000_CHANNEL_1"], ctypes.byref(value))
    assert_pico_ok(status["getSingle"])

    print(f"Channel 1: {value.value} ADC counts")

    if maxADC.value > 0:
        mV = value.value * pl.PL1000_FULL_SCALE_MV / maxADC.value
        print(f"Channel 1: {mV:.1f} mV")

finally:
    # close PicoLog 1000 device
    status["closeUnit"] = pl.pl1000CloseUnit(chandle)
    assert_pico_ok(status["closeUnit"])

# display status returns
print(status)
