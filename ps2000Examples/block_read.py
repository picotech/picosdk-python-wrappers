from ctypes import byref, c_byte, c_int16, c_int32, sizeof
from time import sleep

from picosdk.ps2000 import ps2000
from picosdk.functions import assert_pico2000_ok, adc2mV
from picosdk.PicoDeviceEnums import picoEnum

import matplotlib.pyplot as plt


SAMPLES = 2000
OVERSAMPLING = 1


def get_timebase(device, wanted_time_interval):
    current_timebase = 1

    old_time_interval = None
    time_interval = c_int32(0)
    time_units = c_int16()
    max_samples = c_int32()

    while ps2000.ps2000_get_timebase(
        device.handle,
        current_timebase,
        2000,
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
        ps2000.PS2000_VOLTAGE_RANGE['PS2000_500MV'],
    )
    assert_pico2000_ok(res)

    res = ps2000.ps2000_set_channel(
        device.handle,
        picoEnum.PICO_CHANNEL['PICO_CHANNEL_B'],
        True,
        picoEnum.PICO_COUPLING['PICO_DC'],
        ps2000.PS2000_VOLTAGE_RANGE['PS2000_50MV'],
    )
    assert_pico2000_ok(res)

    timebase_a, interval = get_timebase(device, 4_000)

    collection_time = c_int32()

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
    buffer_b = (c_int16 * SAMPLES)()

    overflow = c_byte(0)

    res = ps2000.ps2000_get_times_and_values(
        device.handle,
        byref(times),
        byref(buffer_a),
        byref(buffer_b),
        None,
        None,
        byref(overflow),
        2,
        SAMPLES,
    )
    assert_pico2000_ok(res)

    channel_a_overflow = (overflow.value & 0b0000_0001) != 0

    ps2000.ps2000_stop(device.handle)

    channel_a_mv = adc2mV(buffer_a, ps2000.PS2000_VOLTAGE_RANGE['PS2000_500MV'], c_int16(32767))
    channel_b_mv = adc2mV(buffer_b, ps2000.PS2000_VOLTAGE_RANGE['PS2000_50MV'], c_int16(32767))

    fig, ax = plt.subplots()
    ax.set_xlabel('time/ms')
    ax.set_ylabel('voltage/mV')
    ax.plot(list(map(lambda x: x * 1e-6, times[:])), channel_a_mv[:])
    ax.plot(list(map(lambda x: x * 1e-6, times[:])), channel_b_mv[:])

    if channel_a_overflow:
        ax.text(0.01, 0.01, 'Overflow present', color='red', transform=ax.transAxes)

    plt.show()
