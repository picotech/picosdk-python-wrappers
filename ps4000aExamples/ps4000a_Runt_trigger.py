import ctypes
from picosdk.ps4000a import ps4000a as ps
from picosdk.functions import assert_pico_ok
import numpy as np

import matplotlib.pyplot as plt
from picosdk.functions import adc2mV,mV2adc

def setup_runt_trigger(chandle, trigger_ch, channel_range_mv):
    # Sets up a positive "Runt" trigger between levels 0v and 1.8V, autotrigger disabled.
    # Assume chandle is already open and channels are set up

    print("Configuring Runt trigger...")
    status = {}
    # 1. Define Trigger Channel Conditions
    # This specifies the Channelto be the source for the trigger logic.
    # PS4000A_CONDITION(source, condition)
    # condition: 0 = Ignore, 1 = True, 2 = False
    cond_list = [
        ps.PS4000A_CONDITION(
            trigger_ch, # ps.PS4000A_CHANNEL["PS4000A_CHANNEL_A"],
            ps.PS4000A_TRIGGER_STATE["PS4000A_TRUE"]
        )
    ]
    # Convert list to ctypes array
    n_cond = len(cond_list)
    conditions = (ps.PS4000A_CONDITION * n_cond)(*cond_list)

    status["setTriggerChannelConditions"] = ps.ps4000aSetTriggerChannelConditions(
        chandle, 
        ctypes.byref(conditions), 
        ctypes.c_int16(n_cond),
        ps.PS4000A_CONDITIONS_INFO["PS4000A_CLEAR"] | ps.PS4000A_CONDITIONS_INFO["PS4000A_ADD"]
    )
    assert_pico_ok(status["setTriggerChannelConditions"])

    # 2. Define Trigger Directions
    # For a Runt trigger, we use "POSITIVE_RUNT" or "NEGATIVE_RUNT".
    # PS4000A_DIRECTION(channel, direction)
    dir_list = [
        ps.PS4000A_DIRECTION(
            trigger_ch, # ps.PS4000A_CHANNEL["PS4000A_CHANNEL_A"],
            ps.PS4000A_THRESHOLD_DIRECTION["PS4000A_POSITIVE_RUNT"]
        )
    ]
    n_dirs = len(dir_list)
    directions = (ps.PS4000A_DIRECTION * n_dirs)(*dir_list)

    status["setTriggerChannelDirections"] = ps.ps4000aSetTriggerChannelDirections(
        chandle,
        ctypes.byref(directions),
        ctypes.c_int16(n_dirs)
    )
    assert_pico_ok(status["setTriggerChannelDirections"])

    # 3. Define Trigger Channel Properties (Thresholds)
    # A runt trigger requires two thresholds (Upper and Lower).
    # Convert mV to ADC counts (helper function assumed or manual calc)
    # For example, if max ADC is 32767:

    lower_threshold_adc = mV2adc(0, channel_range_mv, maxADC)
    print("Lower Threshold: ",lower_threshold_adc)
    upper_threshold_adc = mV2adc(1800, channel_range_mv, maxADC)
    print("Upper Threshold: ",upper_threshold_adc)

    prop_list = [
        ps.PS4000A_TRIGGER_CHANNEL_PROPERTIES(
            ctypes.c_int16(upper_threshold_adc),            # thresholdUpper
            ctypes.c_uint16(256),                           # thresholdUpperHysteresis
            ctypes.c_int16(lower_threshold_adc),            # thresholdLower
            ctypes.c_uint16(256),                           # thresholdLowerHysteresis
            trigger_ch, # ps.PS4000A_CHANNEL["PS4000A_CHANNEL_A"],
            ps.PS4000A_THRESHOLD_MODE["PS4000A_WINDOW"]     # Window type needed for Runt trigger
        )
    ]
    n_props = len(prop_list)
    properties = (ps.PS4000A_TRIGGER_CHANNEL_PROPERTIES * n_props)(*prop_list)

    status["setTriggerChannelProperties"] = ps.ps4000aSetTriggerChannelProperties(
        chandle,
        ctypes.byref(properties),
        ctypes.c_int16(n_props),
        ctypes.c_int16(0),    # auxOutputEnable 0: Off
        ctypes.c_int32(0)  # autoTriggerMilliseconds (0 to wait forever)
    )
    assert_pico_ok(status["setTriggerChannelProperties"])

    # Check with API if trigger is set...
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
    return status

#-------------------------------------------------------------------------------------------
############################################################
# START MAIN CODE

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

channel = ps.PS4000A_CHANNEL["PS4000A_CHANNEL_A"]
chRange = ps.PICO_CONNECT_PROBE_RANGE["PICO_X1_PROBE_5V"] # (see ps4000a.py)

status["setChA"] = ps.ps4000aSetChannel(chandle, ctypes.c_int32(channel), ctypes.c_int16(1), ps.PS4000A_COUPLING["PS4000A_DC"], chRange, ctypes.c_float(0))
assert_pico_ok(status["setChA"])

#########################################################################
setup_runt_trigger(chandle, channel, chRange) # Setup a "Runt "Trigger 
#########################################################################

# Setup number samples and trigger point, and sample interval
preTriggerSamples = 50_000
postTriggerSamples = 50_000
maxSamples = preTriggerSamples + postTriggerSamples

timebase = 400 # ~200kS/s 
# (see Programmer's guide for mre information on timebases)
timeIntervalns = ctypes.c_float()
returnedMaxSamples = ctypes.c_int32()
oversample = ctypes.c_int16(1)
status["getTimebase2"] = ps.ps4000aGetTimebase2(chandle, timebase, maxSamples, ctypes.byref(timeIntervalns), ctypes.byref(returnedMaxSamples), 0)
assert_pico_ok(status["getTimebase2"])
print(status)

#-------------------------------------------------------------------------------------------
# Run block capture
# handle = chandle
# number of pre-trigger samples = preTriggerSamples
# number of post-trigger samples = PostTriggerSamples
# time indisposed ms = None (not needed in the example)
# segment index = 0
# lpReady = None (using ps4000aIsReady rather than ps4000aBlockReady)
# pParameter = None

status["runBlock"] = ps.ps4000aRunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, None, 0, None, None)
assert_pico_ok(status["runBlock"])

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

# Create time data
time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)
time = time/1000000
#fig, (ax1, ax2) = plt.subplots(2, 1) #2 rows 1 column
fig, (ax1) = plt.subplots(1, 1) #1 rows 1 column
# plot data
ax1.plot(time, adc2mVChAMax[:])
ax1.plot(time, adc2mVChBMax[:])
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