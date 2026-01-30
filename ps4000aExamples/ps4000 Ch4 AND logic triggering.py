import ctypes
from ctypes import byref, c_int16, c_int32, sizeof, Structure, c_uint16
import numpy as np
from picosdk.ps4000a import ps4000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV,mV2adc ,assert_pico_ok
from picosdk.errors import PicoSDKCtypesError
import time

nChannels = 4
# Level triggers are limited to any 4 channels by the driver/device! ie (Above/Below "THRESHOLD_DIRECTION")
# Use edge trigger for 5 Channels or more (Rising/falling "THRESHOLD_DIRECTION")

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 4000 series PicoScope
# Returns handle to chandle for use in future API functions
status["openunit"] = ps.ps4000aOpenUnit(ctypes.byref(chandle), None)

try:
    assert_pico_ok(status["openunit"])
except: # PicoNotOkError:
    powerStatus = status["openunit"]

    if powerStatus == 286:
        status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
    elif powerStatus == 282:
        status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
    else:
        raise

    assert_pico_ok(status["changePowerSource"])

maxADC = ctypes.c_int16(0) # (32767)
status["MaximumValue"] = ps.ps4000aMaximumValue(chandle, ctypes.byref(maxADC))
assert_pico_ok(status["MaximumValue"])

# Set up channel A
# handle = chandle
# channel = PS4000a_CHANNEL_A = 0
# enabled = 1
# coupling type = PS4000a_DC = 1
# range = PS4000a_2V = 7
# analogOffset = 0 V
##################chARange = 7
#channel = ctypes.c_int32()
chRange = ctypes.c_int32()
#chARange = 7
#ps.PS4000A_CHANNEL["PS4000A_CHANNEL_A"]
chRange = ps.PICO_CONNECT_PROBE_RANGE["PICO_X1_PROBE_2V"] # pico_x1_probe_2v (see ps4000a.py)
for channel in range(nChannels):   
    status["setCh"] = ps.ps4000aSetChannel(chandle, ctypes.c_int32(channel), ctypes.c_int16(1), ps.PS4000A_COUPLING["PS4000A_DC"], chRange, ctypes.c_float(0))
    assert_pico_ok(status["setCh"])

# Trigger CONDITIONS ####################################
clear = ps.PS4000A_CONDITIONS_INFO["PS4000A_CLEAR"]
add = ps.PS4000A_CONDITIONS_INFO["PS4000A_ADD"] 
action = clear|add

conditions = (ps.PS4000A_CONDITION * nChannels)()  # Array for each channel condition
nConditions = nChannels

######## LOOP #
for channel in range(nChannels):
    conditions[channel].source = ctypes.c_int32(channel)
    conditions[channel].condition = ps.PS4000A_TRIGGER_STATE["PS4000A_TRUE"]

status["setTriggerChannelConditions"] = ps.ps4000aSetTriggerChannelConditions(
chandle,
ctypes.byref(conditions),   # Pass the array by reference
ctypes.c_int16(nConditions), # Pass the length of the array
action                       # Pass the conditions info ##### USE (CLEAR | ADD) on frist call
)
#print("Channel is ", channel)
assert_pico_ok(status["setTriggerChannelConditions"])
###############

# Trigger DIRECTIONS ####################################
directions = (ps.PS4000A_DIRECTION * nChannels)()  # Array for directions (ALL CHANNELS)
nDirections = len(directions)

######## LOOP #
for channel in range(nChannels):
    directions[channel].channel = ctypes.c_int32(channel)
    directions[channel].direction = ps.PS4000A_THRESHOLD_DIRECTION["PS4000A_BELOW"]
###############
  
status["setTriggerChannelDirections"] = ps.ps4000aSetTriggerChannelDirections(
    chandle,
    ctypes.byref(directions),    # Pass the array by reference
    ctypes.c_int16(nDirections), # Pass the length of the array (1 in this case)
)
assert_pico_ok(status["setTriggerChannelDirections"])

# Trigger PROPERTIES ####################################
channelProperties = (ps.PS4000A_TRIGGER_CHANNEL_PROPERTIES * nChannels)() # Array for Properties (ALL CHANNELS)
nChannelProperties = len(channelProperties)

# set trigger properties for channels
# thresholdUpper = mV2adc(300, chRange, maxADC) # Use to set Voltage value
thresholdUpper = int(maxADC.value * 0.5) # (+50% of ADC range) Adjust threshold as needed
thresholdLower = 0  # Adjust threshold as needed
######## LOOP #
for channel in range(nChannels):
    channelProperties[channel].thresholdUpper = ctypes.c_int16(thresholdUpper)
    channelProperties[channel].thresholdUpperHysteresis = ctypes.c_uint16(16) # Adjust hysteresis as needed
    channelProperties[channel].thresholdLower = ctypes.c_int16(thresholdLower)
    channelProperties[channel].thresholdLowerHysteresis = ctypes.c_uint16(16) # Adjust hysteresis as needed
    channelProperties[channel].channel = ctypes.c_int32(channel)
    channelProperties[channel].thresholdMode = ps.PS4000A_THRESHOLD_MODE["PS4000A_LEVEL"]
###############
autoTriggerMilliseconds = 0  # Set to 0 to wait indefinitely for a trigger

status["setTriggerChannelProperties"] = ps.ps4000aSetTriggerChannelProperties(
    chandle,
    ctypes.byref(channelProperties),  # Pass the array by reference
    ctypes.c_int16(nChannelProperties),              # Pass the length of the array
    ctypes.c_int16(0),                              # auxOutputEnable (not used)
    ctypes.c_int32(autoTriggerMilliseconds),        # autoTriggerMilliseconds             ############## PASS as int32 was not working!
)
assert_pico_ok(status["setTriggerChannelProperties"])

#########################################################################

preTriggerSamples = 2500
postTriggerSamples = 2500
maxSamples = preTriggerSamples + postTriggerSamples

timebase = 32
timeIntervalns = ctypes.c_float()
returnedMaxSamples = ctypes.c_int32()
oversample = ctypes.c_int16(1)
status["getTimebase2"] = ps.ps4000aGetTimebase2(chandle, timebase, maxSamples, ctypes.byref(timeIntervalns), ctypes.byref(returnedMaxSamples), 0)
assert_pico_ok(status["getTimebase2"])
print(status)

##################################
triggerEnabled = ctypes.c_int16(0)
pulseWidthQualifierEnabled = ctypes.c_int16(0)

status["isTriggerOrPulseWidthQualifierEnabled"] = ps.ps4000aIsTriggerOrPulseWidthQualifierEnabled(
    chandle, 
    ctypes.byref(triggerEnabled), 
    ctypes.byref(pulseWidthQualifierEnabled)
)

if status["isTriggerOrPulseWidthQualifierEnabled"] == 0:
    if triggerEnabled.value != 0:
        print("Trigger is enabled.")
    else:
        print("Trigger is disabled.")

    if pulseWidthQualifierEnabled.value != 0:
        print("Pulse width qualifier is enabled.")
    else:
        print("Pulse width qualifier is disabled.")
else:
    print("Error checking trigger/pulse width qualifier status.")
#-------------------------------------------------------------------------------------------

# Run block capture
# handle = chandle
# number of pre-trigger samples = preTriggerSamples
# number of post-trigger samples = PostTriggerSamples
# timebase = 3 = 80 ns = timebase (see Programmer's guide for mre information on timebases)
# time indisposed ms = None (not needed in the example)
# segment index = 0
# lpReady = None (using ps4000aIsReady rather than ps4000aBlockReady)
# pParameter = None

status["runBlock"] = ps.ps4000aRunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, None, 0, None, None)
#assert_pico_ok(status["runBlock"])

# Check for data collection to finish using ps4000aIsReady
'''ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
status["isReady"] = ps.ps4000aIsReady(chandle, ctypes.byref(ready))'''
ready = ctypes.c_int16(0)
check = ps.ps4000aIsReady(chandle, ctypes.byref(ready))

while ready.value == 0:  
    #time.sleep(0.01)  # Short delay to allow data capture 
    status["isReady"] = ps.ps4000aIsReady(chandle, ctypes.byref(ready))
    #assert_pico_ok(status["isReady"])
    ###########print(ready.value)


# Create buffers ready for assigning pointers for data collection
bufferAMax = (ctypes.c_int16 * maxSamples)()
bufferAMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example

bufferBMax = (ctypes.c_int16 * maxSamples)()
bufferBMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example

bufferCMax = (ctypes.c_int16 * maxSamples)()
bufferCMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example

bufferDMax = (ctypes.c_int16 * maxSamples)()
bufferDMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example

# Set data buffer location for data collection from channel A
# handle = chandle
# source = PS4000a_CHANNEL_A = 0
# pointer to buffer max = ctypes.byref(bufferAMax)
# pointer to buffer min = ctypes.byref(bufferAMin)
# buffer length = maxSamples
# segementIndex = 0
# mode = PS4000A_RATIO_MODE_NONE = 0

status["setDataBuffersA"] = ps.ps4000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersA"])

status["setDataBuffersB"] = ps.ps4000aSetDataBuffers(chandle, 1, ctypes.byref(bufferBMax), ctypes.byref(bufferBMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersB"])

status["setDataBuffersC"] = ps.ps4000aSetDataBuffers(chandle, 2, ctypes.byref(bufferCMax), ctypes.byref(bufferCMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersC"])

status["setDataBuffersD"] = ps.ps4000aSetDataBuffers(chandle, 3, ctypes.byref(bufferDMax), ctypes.byref(bufferDMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersD"])

# create overflow loaction
overflow = ctypes.c_int16()
# create converted type maxSamples
cmaxSamples = ctypes.c_int32(maxSamples)

# Retried data from scope to buffers assigned above
# handle = chandle
# start index = 0
# pointer to number of samples = ctypes.byref(cmaxSamples)
# downsample ratio = 0
# downsample ratio mode = PS4000a_RATIO_MODE_NONE
# pointer to overflow = ctypes.byref(overflow))
status["getValues"] = ps.ps4000aGetValues(chandle, 0, ctypes.byref(cmaxSamples), 0, 0, 0, ctypes.byref(overflow))
assert_pico_ok(status["getValues"])

# find maximum ADC count value
# handle = chandle
# pointer to value = ctypes.byref(maxADC)

# convert ADC counts data to mV
adc2mVChAMax =  adc2mV(bufferAMax, chRange, maxADC)
adc2mVChBMax =  adc2mV(bufferBMax, chRange, maxADC)
adc2mVChCMax =  adc2mV(bufferCMax, chRange, maxADC)
adc2mVChDMax =  adc2mV(bufferDMax, chRange, maxADC)

# Create time data
time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)
time = time/1000000
#fig, (ax1, ax2) = plt.subplots(2, 1) #2 rows 1 column
fig, (ax1) = plt.subplots(1, 1) #1 rows 1 column
# plot data
ax1.plot(time, adc2mVChAMax[:])
ax1.plot(time, adc2mVChBMax[:])
ax1.plot(time, adc2mVChCMax[:])
ax1.plot(time, adc2mVChDMax[:])
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Voltage (mV)')
ax1.set_title('Channels')
plt.tight_layout()
plt.show()

# Stop the scope
# handle = chandle
status["stop"] = ps.ps4000aStop(chandle)
assert_pico_ok(status["stop"])

# Close unit Disconnect the scope
# handle = chandle
status["close"] = ps.ps4000aCloseUnit(chandle)
assert_pico_ok(status["close"])

# display status returns
print(status)