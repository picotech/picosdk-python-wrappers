import asyncio
import concurrent.futures
import functools

from ctypes import POINTER, c_int16, c_uint32

from picosdk.ps2000 import ps2000
from picosdk.functions import assert_pico2000_ok
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY

from enum import IntEnum


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


CALLBACK = C_CALLBACK_FUNCTION_FACTORY(None, POINTER(POINTER(c_int16)), c_int16, c_uint32, c_int16, c_int16, c_uint32)


# reimplement this because the other one only takes ctypes
def adc_to_mv(values, range_, bitness=16):
    v_ranges = [10, 20, 50, 100, 200, 500, 1_000, 2_000, 5_000, 10_000, 20_000]

    return [(x * v_ranges[range_]) / (2**(bitness - 1) - 1) for x in values]


class StreamingDevice:
    def __init__(self, potential_range=PotentialRange.PS2000_50MV):
        self.device = ps2000.open_unit()
        self.potential_range = potential_range
        # create an event loop
        self.loop = asyncio.new_event_loop()
        # create a thread-pool executor
        self.executor = concurrent.futures.ThreadPoolExecutor()

        self.waiting_blocks = {}

        res = ps2000.ps2000_set_channel(self.device.handle, Channel.PS2000_CHANNEL_A, True, True, potential_range)
        assert_pico2000_ok(res)

        # start 'fast-streaming' mode
        res = ps2000.ps2000_run_streaming_ns(
            self.device.handle,
            100,
            3,
            30_000,
            False,
            1,
            15_000
        )
        assert_pico2000_ok(res)

    async def process_value(self, mv_value):
        # overload
        pass

    def get_streamed_values(self, block_id):
        def get_overview_buffers(buffers, _overflow, _triggered_at, _triggered, _auto_stop, n_values):
            adc_values = buffers[0][0:n_values]

            mv_values = adc_to_mv(adc_values, self.potential_range)

            self.waiting_blocks[block_id] = mv_values

        callback = CALLBACK(get_overview_buffers)

        res = ps2000.ps2000_get_streaming_last_values(
            self.device.handle,
            callback
        )
        assert_pico2000_ok(res)

    def start(self):
        async def gather_values():
            block_id = 0
            while True:
                await asyncio.sleep(0.5)

                await self.loop.run_in_executor(self.executor, functools.partial(self.get_streamed_values, block_id))

                block_id += 1

        async def poll_waiting():
            next_block = 0
            while True:
                if block := self.waiting_blocks.get(next_block):
                    next_block += 1
                    for n in block:
                        await self.process_value(n)

                await asyncio.sleep(0.25)

        try:
            self.loop.create_task(gather_values())
            self.loop.run_until_complete(poll_waiting())
        finally:
            self.loop.close()
            ps2000.ps2000_stop(self.device.handle)
            ps2000.ps2000_close(self.device.handle)


stream = StreamingDevice()
stream.start()
