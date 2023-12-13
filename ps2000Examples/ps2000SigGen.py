import ctypes
import numpy as np
from time import sleep
import math

from picosdk.ps2000 import ps2000 as ps
from picosdk.functions import assert_pico2000_ok, adc2mV
from picosdk.PicoDeviceEnums import picoEnum

import matplotlib.pyplot as plt

import gen_sq_wave as square
import os

# Create status ready for use
status = {}

# Open 2000 series PicoScope
# Returns handle to chandle for use in future API functions
status["openUnit"] = ps.ps2000_open_unit()
assert_pico2000_ok(status["openUnit"])
# Create chandle for use
chandle = ctypes.c_int16(status["openUnit"])

t_sq = np.linspace(0,1,1024)
# waveform = np.array(waveform)
waveform  = square.gen_square(2*np.pi*t_sq, 0.2, 0)

# plot AWG waveform to output
plt.plot(waveform[:])
print("Plotting waveform to output...")
plt.show()
# Once user closes the plot Window the waveform will be output enabled

# change the datatype to ctypes.c_uint8
arbitraryWaveform = waveform.astype('uint8')
arbitraryWaveformSize = ctypes.c_int32(len(waveform))
WaveformSize = len(waveform)

frequecy = 1000 # Hz
print("Frquency is ", frequecy)

# Code to calulate FrequencyToPhase for 2000 series AWG
# deltaPhase=((f*s)/maxBuffer)*phaseAcc*(1/ddsFreq)
# phase =((f*s)/4096)*(32^2)*(1/48000000)
phaseCal = ((frequecy*WaveformSize)/4096)*math.pow(2,32)*(1/48000000)
print("Which converts to AWG Phase value of ", phaseCal)
#Cast float value to interger
phase = ctypes.c_uint32(int(phaseCal))

arbitraryWaveformPointer = arbitraryWaveform.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

print("AWG buffer_length is ", arbitraryWaveformSize)
pkToPk = ctypes.c_uint32(1500000)
offsetVoltage = ctypes.c_int32(0)
sweeps = ctypes.c_uint32(0)
startDeltaPhase = phase
stopDeltaPhase = phase  # when frequency sweep is not required set it equal to startDeltaPhase
deltaPhaseIncrement = ctypes.c_uint32(0)  # when frequency sweep is not required set it to 0
dwellCount = ctypes.c_uint32(0) # when frequency sweep isn't required set it equal to 0
# PS2000_SWEEP_TYPE
#  PS2000_UP 0
#  PS2000_DOWN 1
#  PS2000_UPDOWN 2
#  PS2000_DOWNUP 3
sweepType = 0 #ctypes.c_unt32(0)

print("Output AWG waveform")
status["ps2000_set_sig_gen_arbitrary"] = ps.ps2000_set_sig_gen_arbitrary(chandle, offsetVoltage,
                                                                                pkToPk,
                                                                                startDeltaPhase,
                                                                                stopDeltaPhase,
                                                                                deltaPhaseIncrement,
                                                                                dwellCount,
                                                                                arbitraryWaveformPointer,
                                                                                arbitraryWaveformSize,
                                                                                sweepType,
                                                                                sweeps)
assert_pico2000_ok(status["ps2000_set_sig_gen_arbitrary"])


print("Delay for 10 seconds...")
sleep(10)

# Close unitDisconnect the scope
# handle = chandle
status["close"] = ps.ps2000_close_unit(chandle)
assert_pico2000_ok(status["close"])

# display status returns
print(status)



