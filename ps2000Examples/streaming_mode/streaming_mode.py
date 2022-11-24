from ctypes import POINTER, c_int16, c_uint32

import matplotlib.pyplot as plt
import numpy as np

from picosdk.ps2000 import ps2000
from picosdk.functions import assert_pico2000_ok
from picosdk.PicoDeviceEnums import picoEnum
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY

import time

CALLBACK = C_CALLBACK_FUNCTION_FACTORY(
    None,
    POINTER(POINTER(c_int16)),
    c_int16,
    c_uint32,
    c_int16,
    c_int16,
    c_uint32
)

adc_values = []


def get_overview_buffers(buffers, _overflow, _triggered_at, _triggered, _auto_stop, n_values):
    adc_values.extend(buffers[0][0:n_values])


callback = CALLBACK(get_overview_buffers)


def adc_to_mv(values, range_, bitness=16):
    v_ranges = [10, 20, 50, 100, 200, 500, 1_000, 2_000, 5_000, 10_000, 20_000]

    return [(x * v_ranges[range_]) / (2**(bitness - 1) - 1) for x in values]


with ps2000.open_unit() as device:
    print('Device info: {}'.format(device.info))

    res = ps2000.ps2000_set_channel(
        device.handle,
        picoEnum.PICO_CHANNEL['PICO_CHANNEL_A'],
        True,
        picoEnum.PICO_COUPLING['PICO_DC'],
        ps2000.PS2000_VOLTAGE_RANGE['PS2000_50MV'],
    )
    assert_pico2000_ok(res)

    res = ps2000.ps2000_run_streaming_ns(
        device.handle,
        500,
        2,
        100_000,
        False,
        1,
        50_000
    )
    assert_pico2000_ok(res)

    start_time = time.time_ns()

    while time.time_ns() - start_time < 60_000_000:
        ps2000.ps2000_get_streaming_last_values(
            device.handle,
            callback
        )

    end_time = time.time_ns()

    ps2000.ps2000_stop(device.handle)

    mv_values = adc_to_mv(adc_values, ps2000.PS2000_VOLTAGE_RANGE['PS2000_50MV'])

    fig, ax = plt.subplots()

    ax.set_xlabel('time/ms')
    ax.set_ylabel('voltage/mV')
    ax.plot(np.linspace(0, (end_time - start_time) * 1e-6, len(mv_values)), mv_values)

    plt.show()
