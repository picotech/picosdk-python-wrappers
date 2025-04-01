#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
from __future__ import print_function
from picosdk.discover import find_unit
from picosdk.device import ChannelConfig, TimebaseOptions
import matplotlib.pyplot as plt

with find_unit() as device:

    print("found PicoScope: %s" % (device.info,))

    channel_configs = [ChannelConfig('A', True, 'DC', 5.)]
    microsecond = 1.e-6
    # the entry-level scopes only have about 8k-samples of memory onboard for block mode, so only ask for 6k samples.
    timebase_options = TimebaseOptions(microsecond, None, 6000 * microsecond)

    times, voltages, overflow_warnings = device.capture_block(timebase_options, channel_configs)

    for channel, data in voltages.items():
        label = "Channel %s" % channel
        if channel in overflow_warnings:
            label += " (over range)"
        plt.plot(times, data, label=label)

    plt.xlabel('Time / s')
    plt.ylabel('Amplitude / V')
    plt.legend()
    plt.show()

