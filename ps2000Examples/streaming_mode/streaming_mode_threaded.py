from ctypes import POINTER, c_int16, c_uint32

from picosdk.ps2000 import ps2000
from picosdk.functions import assert_pico2000_ok
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY

from enum import IntEnum
from concurrent.futures import ThreadPoolExecutor

import functools
import time
import os

CALLBACK = C_CALLBACK_FUNCTION_FACTORY(None, POINTER(POINTER(c_int16)), c_int16, c_uint32, c_int16, c_int16, c_uint32)

THREADPOOL = ThreadPoolExecutor()

past_mv_values = []

term_width = os.get_terminal_size()


def process_values(adc_values):
    mv_values = adc_to_mv(adc_values, PotentialRange.PS2000_50MV)

    for value in mv_values:
        pre = (value + 500) / 500 * term_width
        print('{}|'.format(' ' * pre))

    past_mv_values.extend(mv_values)


def get_overview_buffers(buffers, _overflow, _triggered_at, _triggered, _auto_stop, n_values):
    adc_values = buffers[0][0:n_values]

    THREADPOOL.submit(functools.partial(process_values, adc_values))


callback = CALLBACK(get_overview_buffers)


def adc_to_mv(values, range_, bitness=16):
    v_ranges = [10, 20, 50, 100, 200, 500, 1_000, 2_000, 5_000, 10_000, 20_000]

    return [(x * v_ranges[range_]) / (2**(bitness - 1) - 1) for x in values]


class Channel(IntEnum):
    PS2000_CHANNEL_A = 0
    PS2000_CHANNEL_B = 1


class PotentialRange(IntEnum):
    PS2000_20MV = 1
    PS2000_50MV = 2
    PS2000_100MV = 3
    PS2000_200MV = 4
    PS2000_500MV = 5
    PS2000_1V = 6
    PS2000_2V = 7
    PS2000_5V = 8
    PS2000_10V = 9
    PS2000_20V = 10


with ps2000.open_unit() as device:
    res = ps2000.ps2000_set_channel(device.handle, Channel.PS2000_CHANNEL_A, True, True, PotentialRange.PS2000_50MV)
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

    target_samples = 1_000_000

    while True:
        ps2000.ps2000_get_streaming_last_values(
            device.handle,
            callback
        )

        time.sleep(0.01)
