from ctypes import byref, c_int16, c_int32, sizeof, Structure, c_uint16
from time import sleep

import numpy as np
from picosdk.ps2000 import ps2000
from picosdk.functions import assert_pico2000_ok, adc2mV
from picosdk.PicoDeviceEnums import picoEnum

import matplotlib.pyplot as plt

SAMPLES = 2000
OVERSAMPLING = 1
PRESAMPLE = 80.0
ADC_THRESHOLDS = (12000, 2048)

THRESHOLD_DIRECTION = {
    'PS2000_ABOVE': 0,
    'PS2000_BELOW': 1,
    'PS2000_ADV_RISING': 2,
    'PS2000_ADV_FALLING': 3,
    'PS2000_ADV_RISING_OR_FALLING': 4,
    'PS2000_INSIDE': 0,
    'PS2000_OUTSIDE': 1,
    'PS2000_ENTER': 2,
    'PS2000_EXIT': 3,
    'PS2000_ENTER_OR_EXIT': 4,
    'PS2000_ADV_NONE': 2,
}


class TriggerConditions(Structure):
    _fields_ = [
        ('channelA', c_int32),
        ('channelB', c_int32),
        ('channelC', c_int32),
        ('channelD', c_int32),
        ('external', c_int32),
        ('pulseWidthQualifier', c_int32),
    ]


class PwqConditions(Structure):
    _fields_ = [
        ('channelA', c_int32),
        ('channelB', c_int32),
        ('channelC', c_int32),
        ('channelD', c_int32),
        ('external', c_int32),
    ]


class TriggerChannelProperties(Structure):
    _fields_ = [
        ("thresholdMajor", c_int16),
        ("thresholdMinor", c_int16),
        ("hysteresis", c_uint16),
        ("channel", c_int16),
        ("thresholdMode", c_int16),
    ]


def get_timebase(device, wanted_time_interval):
    current_timebase = 1

    old_time_interval = None
    time_interval = c_int32(0)
    time_units = c_int16()
    max_samples = c_int32()

    while ps2000.ps2000_get_timebase(
        device.handle,
        current_timebase,
        SAMPLES,
        byref(time_interval),
        byref(time_units),
        1,
        byref(max_samples)) == 0 \
        or time_interval.value < wanted_time_interval:

        current_timebase += 1
        old_time_interval = time_interval.value

        if current_timebase.bit_length() > sizeof(c_int16) * 8:
            raise Exception('No appropriate timebase was identifiable')

    return current_timebase - 1, old_time_interval


with ps2000.open_unit() as device:
    print('Device info: {}'.format(device.info))

    res = ps2000.ps2000_set_channel(
        device.handle,
        picoEnum.PICO_CHANNEL['PICO_CHANNEL_A'],
        True,
        picoEnum.PICO_COUPLING['PICO_DC'],
        ps2000.PS2000_VOLTAGE_RANGE['PS2000_500MV']
    )
    assert_pico2000_ok(res)

    trigger_conditions = TriggerConditions(0, 0, 0, 0, 0, 1)

    res = ps2000.ps2000SetAdvTriggerChannelConditions(device.handle, byref(trigger_conditions), 1)
    assert_pico2000_ok(res)

    res = ps2000.ps2000SetAdvTriggerDelay(device.handle, 0, -PRESAMPLE)
    assert_pico2000_ok(res)

    res = ps2000.ps2000SetAdvTriggerChannelDirections(
        device.handle,
        THRESHOLD_DIRECTION['PS2000_EXIT'],
        THRESHOLD_DIRECTION['PS2000_ADV_NONE'],
        THRESHOLD_DIRECTION['PS2000_ADV_NONE'],
        THRESHOLD_DIRECTION['PS2000_ADV_NONE'],
        THRESHOLD_DIRECTION['PS2000_ADV_NONE']
    )
    assert_pico2000_ok(res)

    trigger_properties = TriggerChannelProperties(
        max(ADC_THRESHOLDS),
        min(ADC_THRESHOLDS),
        328,
        ps2000.PS2000_CHANNEL['PS2000_CHANNEL_A'],
        picoEnum.PICO_THRESHOLD_MODE['PICO_WINDOW']
    )

    res = ps2000.ps2000SetAdvTriggerChannelProperties(device.handle, byref(trigger_properties), 1, 0)
    assert_pico2000_ok(res)

    pwq_conditions = PwqConditions(1, 0, 0, 0, 0)

    res = ps2000.ps2000SetPulseWidthQualifier(
        device.handle,
        byref(pwq_conditions),
        1,
        THRESHOLD_DIRECTION['PS2000_ENTER'],
        100,
        0,
        picoEnum.PICO_PULSE_WIDTH_TYPE['PICO_PW_TYPE_GREATER_THAN']
    )
    assert_pico2000_ok(res)

    timebase_a, interval = get_timebase(device, 4_000)

    collection_time = c_int32()

    fig, ax = plt.subplots()
    ax.set_xlabel('time/ms')
    ax.set_ylabel('ADC counts')

    res = ps2000.ps2000_run_block(
        device.handle,
        SAMPLES,
        timebase_a,
        OVERSAMPLING,
        byref(collection_time)
    )
    assert_pico2000_ok(res)

    while ps2000.ps2000_ready(device.handle) == 0:
        sleep(0.1)

    times = (c_int32 * SAMPLES)()

    buffer_a = (c_int16 * SAMPLES)()

    res = ps2000.ps2000_get_times_and_values(
        device.handle,
        byref(times),
        byref(buffer_a),
        None,
        None,
        None,
        None,
        2,
        SAMPLES,
    )
    assert_pico2000_ok(res)

    channel_a_mv = adc2mV(buffer_a, ps2000.PS2000_VOLTAGE_RANGE['PS2000_50MV'], c_int16(32767))

    ax.plot(list(map(lambda x: x * 1e-6, times[:])), buffer_a[:])
    for threshold in ADC_THRESHOLDS:
        ax.plot(list(map(lambda x: x * 1e-6, times[:])), [threshold for _ in times[:]], color='red')

    ax.axvline(np.percentile(list(map(lambda x: x * 1e-6, times[:])), PRESAMPLE), color='red', linestyle='dotted')

    ps2000.ps2000_stop(device.handle)

    plt.show()
