from time import time_ns
from ctypes import POINTER, c_int16, c_uint32

import matplotlib.pyplot as plt
import numpy as np

from picosdk.ps2000 import ps2000
from picosdk.functions import assert_pico2000_ok
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY

from enum import IntEnum


class Channel(IntEnum):
    PS2000_CHANNEL_A = 0
    PS2000_CHANNEL_B = 1


class PotentialRange(IntEnum):
    PS2000_10MV = 0
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


class TimeUnit(IntEnum):
    FEMTOSECOND = 0
    PICOSECOND = 1
    NANOSECOND = 2
    MICROSECOND = 3
    MILLISECOND = 4
    SECOND = 5


CALLBACK = C_CALLBACK_FUNCTION_FACTORY(None, POINTER(POINTER(c_int16)), c_int16, c_uint32, c_int16, c_int16, c_uint32)


# reimplement this because the other one only takes ctypes
def adc_to_mv(values, range_, bitness=16):
    v_ranges = [10, 20, 50, 100, 200, 500, 1_000, 2_000, 5_000, 10_000, 20_000]

    return [(x * v_ranges[range_]) / (2**(bitness - 1) - 1) for x in values]


def determine_time_unit(interval_ns):
    unit = 0
    units = ['ns', 'us', 'ms', 's']

    while interval_ns > 5_000:
        interval_ns /= 1000
        unit += 1

    return interval_ns, units[unit]


class StreamingDevice:
    def __init__(self, gather_values, potential_range=PotentialRange.PS2000_50MV):
        self.device = ps2000.open_unit()
        self.potential_range = potential_range

        self.gather_values = gather_values

        res = ps2000.ps2000_set_channel(self.device.handle, Channel.PS2000_CHANNEL_A, True, True, potential_range)
        assert_pico2000_ok(res)

        # start 'fast-streaming' mode
        res = ps2000.ps2000_run_streaming_ns(
            self.device.handle,
            500,
            TimeUnit.NANOSECOND,
            100_000,
            False,
            1,
            50_000
        )
        assert_pico2000_ok(res)

        self.start_time = time_ns()
        self.end_time = time_ns()

    def close(self):
        ps2000.ps2000_stop(self.device.handle)
        self.device.close()

    def gather(self):
        adc_values = []

        def get_overview_buffers(buffers, _overflow, _triggered_at, _triggered, _auto_stop, n_values):
            adc_values.extend(buffers[0][0:n_values])

        callback = CALLBACK(get_overview_buffers)

        while len(adc_values) < self.gather_values:
            ps2000.ps2000_get_streaming_last_values(
                self.device.handle,
                callback
            )

        self.end_time = time_ns()

        return adc_to_mv(adc_values, self.potential_range)


stream = StreamingDevice(6_000_000)
values = stream.gather()
stream.close()

print('Values gathered: {}'.format(len(values)))

fig, ax = plt.subplots()
interval, units = determine_time_unit(stream.end_time - stream.start_time)

ax.set_xlabel('time/{}'.format(units))
ax.set_ylabel('voltage/mV')
ax.plot(np.linspace(0, interval, len(values)), values)

plt.show()
