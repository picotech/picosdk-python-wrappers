#
# Copyright (C) 2015-2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps2000.h C header file
for PicoScope 2000 Series oscilloscopes using the ps2000 driver API functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.errors import ArgumentOutOfRangeError
from picosdk.constants import make_enum


class Ps2000lib(Library):
    def __init__(self):
        super(Ps2000lib, self).__init__("ps2000")


ps2000 = Ps2000lib()

ps2000.PS2000_CHANNEL = make_enum([
    "PS2000_CHANNEL_A",
    "PS2000_CHANNEL_B",
])

# use the last character, i.e. the channel name:
ps2000.PICO_CHANNEL = {k[-1]: v for k, v in ps2000.PS2000_CHANNEL.items()}

# This field is passed to the driver as a boolean, not an enum.
ps2000.PICO_COUPLING = {
    'AC': 0,
    'DC': 1
}

ps2000.PS2000_VOLTAGE_RANGE = {
    'PS2000_20MV':  1,
    'PS2000_50MV':  2,
    'PS2000_100MV': 3,
    'PS2000_200MV': 4,
    'PS2000_500MV': 5,
    'PS2000_1V':    6,
    'PS2000_2V':    7,
    'PS2000_5V':    8,
    'PS2000_10V':   9,
    'PS2000_20V':   10,
}

# float voltage value max (multiplier for output voltages). Parse the value in the constant name.
ps2000.PICO_VOLTAGE_RANGE = {
    v: float(k.split('_')[1][:-1]) if k[-2] != 'M' else (0.001 * float(k.split('_')[1][:-2]))
    for k, v in ps2000.PS2000_VOLTAGE_RANGE.items()
}

ps2000.MAX_MEMORY = 32e3

doc = """ int16_t ps2000_open_unit
    (
        void
    ); """
ps2000.make_symbol("_open_unit", "ps2000_open_unit", c_int16, [], doc)

doc = """ int16_t ps2000_get_unit_info
    (
        int16_t  handle,
        int8_t  *string,
        int16_t  string_length,
        int16_t  line
    ); """
ps2000.make_symbol("_get_unit_info", "ps2000_get_unit_info", c_int16, [c_int16, c_char_p, c_int16, c_int16], doc)

doc = """ int16_t ps2000_flash_led
    (
        int16_t handle
    ); """
ps2000.make_symbol("_flash_led", "ps2000_flash_led", c_int16, [c_int16, ], doc)

doc = """ int16_t ps2000_close_unit
    (
        int16_t handle
    ); """
ps2000.make_symbol("_close_unit", "ps2000_close_unit", c_int16, [c_int16, ], doc)

doc = """ int16_t ps2000_set_channel
    (
        int16_t  handle,
        int16_t  channel,
        int16_t  enabled,
        int16_t  dc,
        int16_t  range
    ); """
ps2000.make_symbol("_set_channel", "ps2000_set_channel", c_int16, [c_int16, c_int16, c_int16, c_int16, c_int16], doc)

doc = """ int16_t ps2000_get_timebase
    (
        int16_t  handle,
        int16_t  timebase,
        int32_t  no_of_samples,
        int32_t *time_interval,
        int16_t *time_units,
        int16_t  oversample,
        int32_t *max_samples
    ); """
ps2000.make_symbol("_get_timebase", "ps2000_get_timebase", c_int16,
                   [c_int16, c_int16, c_int32, c_void_p, c_void_p, c_int16, c_void_p], doc)

doc = """ int16_t ps2000_set_trigger
    (
        int16_t  handle,
        int16_t  source,
        int16_t  threshold,
        int16_t  direction,
        int16_t  delay,
        int16_t  auto_trigger_ms
    ); """
ps2000.make_symbol("_set_trigger", "ps2000_set_trigger", c_int16,
                   [c_int16, c_int16, c_int16, c_int16, c_int16, c_int16], doc)

doc = """ int16_t ps2000_set_trigger2
    (
        int16_t  handle,
        int16_t  source,
        int16_t  threshold,
        int16_t  direction,
        float    delay,
        int16_t  auto_trigger_ms
    ); """
ps2000.make_symbol("_set_trigger2", "ps2000_set_trigger2", c_int16,
                   [c_int16, c_int16, c_int16, c_int16, c_float, c_int16], doc)

doc = """ int16_t ps2000_run_block
    (
        int16_t handle,
        int32_t  no_of_values,
        int16_t  timebase,
        int16_t  oversample,
        int32_t * time_indisposed_ms
    ); """
ps2000.make_symbol("_run_block", "ps2000_run_block", c_int16, [c_int16, c_int32, c_int16, c_int16, c_void_p], doc)

doc = """ int16_t ps2000_run_streaming
    (
        int16_t  handle,
        int16_t  sample_interval_ms,
        int32_t  max_samples,
        int16_t  windowed
    ); """
ps2000.make_symbol("_run_streaming", "ps2000_run_streaming", c_int16, [c_int16, c_int16, c_int32, c_int16], doc)

doc = """ int16_t ps2000_run_streaming_ns
    (
        int16_t            handle,
        uint32_t           sample_interval,
        PS2000_TIME_UNITS  time_units,
        uint32_t           max_samples,
        int16_t            auto_stop,
        uint32_t           noOfSamplesPerAggregate,
        uint32_t           overview_buffer_size
    ); """
ps2000.make_symbol("_run_streaming_ns", "ps2000_run_streaming_ns", c_int16,
                   [c_int16, c_uint32, c_int32, c_uint32, c_int16, c_uint32, c_uint32], doc)

doc = """ int16_t ps2000_ready
    (
        int16_t  handle
    ); """
ps2000.make_symbol("_ready", "ps2000_ready", c_int16, [c_int16, ], doc)

doc = """ int16_t ps2000_stop
    (
        int16_t  handle
    ); """
ps2000.make_symbol("_stop", "ps2000_stop", c_int16, [c_int16, ], doc)

doc = """ int32_t ps2000_get_values
    (
        int16_t  handle,
        int16_t *buffer_a,
        int16_t *buffer_b,
        int16_t *buffer_c,
        int16_t *buffer_d,
        int16_t *overflow,
        int32_t  no_of_values
    ); """
ps2000.make_symbol("_get_values", "ps2000_get_values", c_int32,
                   [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_int32], doc)

doc = """ int32_t ps2000_get_times_and_values
    (
        int16_t  handle,
        int32_t *times,
        int16_t *buffer_a,
        int16_t *buffer_b,
        int16_t *buffer_c,
        int16_t *buffer_d,
        int16_t *overflow,
        int16_t  time_units,
        int32_t  no_of_values
    ); """
ps2000.make_symbol("_get_times_and_values", "ps2000_get_times_and_values", c_int32,
                   [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_int16, c_int32], doc)

doc = """ int16_t ps2000_last_button_press
    (
        int16_t  handle
    ); """
ps2000.make_symbol("_last_button_press", "ps2000_last_button_press", c_int16, [c_int16, ], doc)

doc = """ int32_t ps2000_set_ets
    (
        int16_t  handle,
        int16_t  mode,
        int16_t  ets_cycles,
        int16_t  ets_interleave
    ); """
ps2000.make_symbol("_set_ets", "ps2000_set_ets", c_int32, [c_int16, c_int16, c_int16, c_int16], doc)

doc = """ int16_t ps2000_set_led
    (
        int16_t  handle,
        int16_t  state
    ); """
ps2000.make_symbol("_set_led", "ps2000_set_led", c_int16, [c_int16, c_int16], doc)

doc = """ int16_t ps2000_open_unit_async
    (
        void
    ); """
ps2000.make_symbol("_open_unit_async", "ps2000_open_unit_async", c_int16, [], doc)

doc = """ int16_t ps2000_open_unit_progress
    (
        int16_t *handle,
        int16_t *progress_percent
    ); """
ps2000.make_symbol("_open_unit_progress", "ps2000_open_unit_progress", c_int16, [c_void_p, c_void_p], doc)

doc = """ int16_t ps2000_get_streaming_last_values
    (
        int16_t  handle,
        GetOverviewBuffersMaxMin
    ); """
ps2000.make_symbol("_get_streaming_last_values", "ps2000_get_streaming_last_values", c_int16, [c_int16, c_void_p], doc)

doc = """ int16_t ps2000_overview_buffer_status
    (
        int16_t  handle,
        int16_t *previous_buffer_overrun
    ); """
ps2000.make_symbol("_overview_buffer_status", "ps2000_overview_buffer_status", c_int16, [c_int16, c_void_p], doc)

doc = """ uint32_t ps2000_get_streaming_values
    (
        int16_t  handle,
        double   *start_time,
        int16_t  *pbuffer_a_max,
        int16_t  *pbuffer_a_min,
        int16_t  *pbuffer_b_max,
        int16_t  *pbuffer_b_min,
        int16_t  *pbuffer_c_max,
        int16_t  *pbuffer_c_min,
        int16_t  *pbuffer_d_max,
        int16_t  *pbuffer_d_min,
        int16_t  *overflow,
        uint32_t *triggerAt,
        int16_t  *triggered,
        uint32_t  no_of_values,
        uint32_t  noOfSamplesPerAggregate
    ); """
ps2000.make_symbol("_get_streaming_values", "ps2000_get_streaming_values", c_uint32,
                   [c_int16, c_void_p,
                    c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p,
                    c_void_p, c_void_p, c_void_p, c_uint32, c_uint32], doc)

doc = """ uint32_t ps2000_get_streaming_values_no_aggregation
    (
        int16_t handle,
        double *start_time,
        int16_t * pbuffer_a,
        int16_t * pbuffer_b,
        int16_t * pbuffer_c,
        int16_t * pbuffer_d,
        int16_t * overflow,
        uint32_t * triggerAt,
        int16_t * trigger,
        uint32_t no_of_values
    ); """
ps2000.make_symbol("_get_streaming_values_no_aggregation", "ps2000_get_streaming_values_no_aggregation", c_uint32,
                   [c_int16, c_void_p,
                    c_void_p, c_void_p, c_void_p, c_void_p,
                    c_void_p, c_void_p, c_void_p, c_uint32], doc)

doc = """ int16_t ps2000_set_light
    (
        int16_t  handle,
        int16_t  state
    ); """
ps2000.make_symbol("_set_light", "ps2000_set_light", c_int16, [c_int16, c_int16], doc)

doc = """ int16_t ps2000_set_sig_gen_arbitrary
    (
        int16_t            handle,
        int32_t            offsetVoltage,
        uint32_t           pkToPk,
        uint32_t           startDeltaPhase,
        uint32_t           stopDeltaPhase,
        uint32_t           deltaPhaseIncrement,
        uint32_t           dwellCount,
        uint8_t           *arbitraryWaveform,
        int32_t            arbitraryWaveformSize,
        PS2000_SWEEP_TYPE  sweepType,
        uint32_t           sweeps
    ); """
ps2000.make_symbol("_set_sig_gen_arbitrary", "ps2000_set_sig_gen_arbitrary", c_int16,
                   [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p, c_int32, c_int32,
                    c_uint32], doc)

doc = """ int16_t ps2000_set_sig_gen_built_in
    (
        int16_t            handle,
        int32_t            offsetVoltage,
        uint32_t           pkToPk,
        PS2000_WAVE_TYPE   waveType,
        float              startFrequency,
        float              stopFrequency,
        float              increment,
        float              dwellTime,
        PS2000_SWEEP_TYPE  sweepType,
        uint32_t           sweeps
    ); """
ps2000.make_symbol("_set_sig_gen_built_in", "ps2000_set_sig_gen_built_in", c_int16,
                   [c_int16, c_int32, c_uint32, c_int32, c_float, c_float, c_float, c_float, c_int32, c_uint32], doc)

doc = """ int16_t ps2000SetAdvTriggerChannelProperties
    (
        int16_t                            handle,
        PS2000_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                            nChannelProperties,
        int32_t                            autoTriggerMilliseconds
    ); """
ps2000.make_symbol("_SetAdvTriggerChannelProperties", "ps2000SetAdvTriggerChannelProperties", c_int16,
                   [c_int16, c_void_p, c_int16, c_int32], doc)

doc = """ int16_t ps2000SetAdvTriggerChannelConditions
    (
        int16_t                    handle,
        PS2000_TRIGGER_CONDITIONS *conditions,
        int16_t                    nConditions
    ); """
ps2000.make_symbol("_SetAdvTriggerChannelConditions", "ps2000SetAdvTriggerChannelConditions", c_int16,
                   [c_int16, c_void_p, c_int16], doc)

doc = """ int16_t ps2000SetAdvTriggerChannelDirections
    (
        int16_t                     handle,
        PS2000_THRESHOLD_DIRECTION  channelA,
        PS2000_THRESHOLD_DIRECTION  channelB,
        PS2000_THRESHOLD_DIRECTION  channelC,
        PS2000_THRESHOLD_DIRECTION  channelD,
        PS2000_THRESHOLD_DIRECTION  ext
    ); """
ps2000.make_symbol("_SetAdvTriggerChannelDirections", "ps2000SetAdvTriggerChannelDirections", c_int16,
                   [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32], doc)

doc = """ int16_t ps2000SetPulseWidthQualifier
    (
        int16_t                     handle,
        PS2000_PWQ_CONDITIONS      *conditions,
        int16_t                     nConditions,
        PS2000_THRESHOLD_DIRECTION  direction,
        uint32_t                    lower,
        uint32_t                    upper,
        PS2000_PULSE_WIDTH_TYPE     type
    ); """
ps2000.make_symbol("_SetPulseWidthQualifier", "ps2000SetPulseWidthQualifier", c_int16,
                   [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32], doc)

doc = """ int16_t ps2000SetAdvTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay,
        float     preTriggerDelay
    ); """
ps2000.make_symbol("_SetAdvTriggerDelay", "ps2000SetAdvTriggerDelay", c_int16, [c_int16, c_uint32, c_float], doc)

doc = """ int16_t ps2000PingUnit
    (
        int16_t  handle
    ); """
ps2000.make_symbol("_PingUnit", "ps2000PingUnit", c_int16, [c_int16, ], doc)

ps2000.PICO_INFO = {k: v for k, v in ps2000.PICO_INFO.items() if v <= 0x00000005}
ps2000.PICO_INFO["PICO_ERROR_CODE"] = 0x00000006
ps2000.PICO_INFO["PICO_KERNEL_DRIVER_VERSION"] = 0x00000007
