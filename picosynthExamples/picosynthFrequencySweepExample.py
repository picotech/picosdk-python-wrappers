#
# Copyright (C) 2022 Pico Technology Ltd. See LICENSE file for terms.
#
# PicoSource AS108 Agile Synthesizer Example
# This example demonstrates how to use the PicoSource AS108 picosynth driver API functions to set up the signal generator to output a frequency sweep.
#

import ctypes
from picosdk.picosynth import picosynth as ps
import time
from picosdk.functions import assert_pico_ok

# setup needed variables
status = {}
chandle = ctypes.c_uint32()

# open AS108 device
status["openunit"] = ps.picosynthOpenUnit(ps.PICO_SOURCE_MODEL["PICO_SYNTH"], ctypes.byref(chandle),0)
assert_pico_ok(status["openunit"])

# set up a frequency sweep
# handle = chandle
startFreqHz = 300000 #Hz
stopFreqHz = 1000000 #Hz
startLevel = 2
stopLevel = 2
levelUnit = 1 # VoltsPkToPk
dwellTimeUs = 100
pointsInSweep = 1000
mode = 0 #SweepAndFlyback
triggerMode = 0 # InternalTrigger

status["setFrequencyAndLevelSweep"] = ps.picosynthSetFrequencyAndLevelSweep(chandle,startFreqHz,stopFreqHz,startLevel,stopLevel,levelUnit,dwellTimeUs,pointsInSweep,mode,triggerMode)
assert_pico_ok(status["setFrequencyAndLevelSweep"])

time.sleep(10)

# close AS108 device
status["closeunit"] = ps.picosynthCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

time.sleep(20)

# open AS108 device
status["openunit"] = ps.picosynthOpenUnit(ps.PICO_SOURCE_MODEL["PICO_SYNTH"], ctypes.byref(chandle),0)
assert_pico_ok(status["openunit"])

# set output off
status["setOutputOff"] = ps.picosynthSetOutputOff(chandle)

# close AS108 device
status["closeunit"] = ps.picosynthCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

# Displays the status returns
print(status)