#
# Copyright (C) 2015-2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps3000.h C header file
for PicoScope 3000 Series oscilloscopes using the ps3000 driver API functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.constants import make_enum


class Ps3000lib(Library):
    def __init__(self):
        super(Ps3000lib, self).__init__("ps3000")


ps3000 = Ps3000lib()

ps3000.PS3000_CHANNEL = make_enum([
    "PS3000_CHANNEL_A",
    "PS3000_CHANNEL_B",
    "PS3000_CHANNEL_C",
    "PS3000_CHANNEL_D",
])

# use the last character, i.e. the channel name:
ps3000.PICO_CHANNEL = {k[-1]: v for k, v in ps3000.PS3000_CHANNEL.items()}

# This field is passed to the driver as a boolean, not an enum.
ps3000.PICO_COUPLING = {
    'AC': 0,
    'DC': 1
}

ps3000.PS3000_VOLTAGE_RANGE = {
    'PS3000_20MV':  1,
    'PS3000_50MV':  2,
    'PS3000_100MV': 3,
    'PS3000_200MV': 4,
    'PS3000_500MV': 5,
    'PS3000_1V':    6,
    'PS3000_2V':    7,
    'PS3000_5V':    8,
    'PS3000_10V':   9,
    'PS3000_20V':   10,
    'PS3000_50V':   11,
    'PS3000_100V':  12,
    'PS3000_200V':  13,
    'PS3000_400V':  14,
}

# float voltage value max (multiplier for output voltages). Parse the value in the constant name.
ps3000.PICO_VOLTAGE_RANGE = {
    v: float(k.split('_')[1][:-1]) if k[-2] != 'M' else (0.001 * float(k.split('_')[1][:-2]))
    for k, v in ps3000.PS3000_VOLTAGE_RANGE.items()
}

doc = """ int16_t ps3000_open_unit
    (
        void
    ); """
ps3000.make_symbol("_open_unit", "ps3000_open_unit", c_int16, [], doc)

doc = """ int16_t ps3000_get_unit_info
    (
        int16_t  handle,
        int8_t  *string,
        int16_t  string_length,
        int16_t  line
    ); """
ps3000.make_symbol("_get_unit_info", "ps3000_get_unit_info", c_int16, [c_int16, c_char_p, c_int16, c_int16], doc)

doc = """ int16_t ps3000_flash_led
    (
        int16_t handle
    ); """
ps3000.make_symbol("_flash_led", "ps3000_flash_led", c_int16, [c_int16, ], doc)

doc = """ int16_t ps3000_close_unit
    (
        int16_t handle
    ); """
ps3000.make_symbol("_close_unit", "ps3000_close_unit", c_int16, [c_int16, ], doc)

doc = """ int16_t ps3000_set_channel
    (
        int16_t  handle,
        int16_t  channel,
        int16_t  enabled,
        int16_t  dc,
        int16_t  range
    ); """
ps3000.make_symbol("_set_channel", "ps3000_set_channel", c_int16, [c_int16, c_int16, c_int16, c_int16, c_int16], doc)

doc = """ int16_t ps3000_get_timebase
    (
        int16_t  handle,
        int16_t  timebase,
        int32_t  no_of_samples,
        int32_t *time_interval,
        int16_t *time_units,
        int16_t  oversample,
        int32_t *max_samples
    ); """
ps3000.make_symbol("_get_timebase", "ps3000_get_timebase", c_int16,
                   [c_int16, c_int16, c_int32, c_void_p, c_void_p, c_int16, c_void_p], doc)

doc = """ int32_t ps3000_set_siggen
    (
        int16_t  handle,
        int16_t  wave_type,
        int32_t  start_frequency,
        int32_t  stop_frequency,
        float    increment,
        int16_t  dwell_time,
        int16_t  repeat,
        int16_t  dual_slope
    ); """
ps3000.make_symbol("_set_siggen", "ps3000_set_siggen", c_int32,
                   [c_int16, c_int16, c_int32, c_int32, c_float, c_int16, c_int16, c_int16], doc)

doc = """ int32_t ps3000_set_ets
    (
        int16_t  handle,
        int16_t  mode,
        int16_t  ets_cycles,
        int16_t  ets_interleave
    ); """
ps3000.make_symbol("_set_ets", "ps3000_set_ets", c_int32, [c_int16, c_int16, c_int16, c_int16], doc)

doc = """ int16_t ps3000_set_trigger
    (
        int16_t  handle,
        int16_t  source,
        int16_t  threshold,
        int16_t  direction,
        int16_t  delay,
        int16_t  auto_trigger_ms
    ); """
ps3000.make_symbol("_set_trigger", "ps3000_set_trigger", c_int16,
                   [c_int16, c_int16, c_int16, c_int16, c_int16, c_int16], doc)

doc = """ int16_t ps3000_set_trigger2
    (
        int16_t  handle,
        int16_t  source,
        int16_t  threshold,
        int16_t  direction,
        float    delay,
        int16_t  auto_trigger_ms
    ); """
ps3000.make_symbol("_set_trigger2", "ps3000_set_trigger2", c_int16,
                   [c_int16, c_int16, c_int16, c_int16, c_float, c_int16], doc)

doc = """ int16_t ps3000_run_block
    (
        int16_t handle,
        int32_t  no_of_values,
        int16_t  timebase,
        int16_t  oversample,
        int32_t * time_indisposed_ms
    ); """
ps3000.make_symbol("_run_block", "ps3000_run_block", c_int16, [c_int16, c_int32, c_int16, c_int16, c_void_p], doc)

doc = """ int16_t ps3000_run_streaming
    (
        int16_t  handle,
        int16_t  sample_interval_ms,
        int32_t  max_samples,
        int16_t  windowed
    ); """
ps3000.make_symbol("_run_streaming", "ps3000_run_streaming", c_int16, [c_int16, c_int16, c_int32, c_int16], doc)

doc = """ int16_t ps3000_run_streaming_ns
    (
        int16_t            handle,
        uint32_t           sample_interval,
        PS3000_TIME_UNITS  time_units,
        uint32_t           max_samples,
        int16_t            auto_stop,
        uint32_t           noOfSamplesPerAggregate,
        uint32_t           overview_buffer_size
    ); """
ps3000.make_symbol("_run_streaming_ns", "ps3000_run_streaming_ns", c_int16,
                   [c_int16, c_uint32, c_int32, c_uint32, c_int16, c_uint32, c_uint32], doc)

doc = """ int16_t ps3000_ready
    (
        int16_t  handle
    ); """
ps3000.make_symbol("_ready", "ps3000_ready", c_int16, [c_int16, ], doc)

doc = """ int16_t ps3000_stop
    (
        int16_t  handle
    ); """
ps3000.make_symbol("_stop", "ps3000_stop", c_int16, [c_int16, ], doc)

doc = """ int32_t ps3000_get_values
    (
        int16_t  handle,
        int16_t *buffer_a,
        int16_t *buffer_b,
        int16_t *buffer_c,
        int16_t *buffer_d,
        int16_t *overflow,
        int32_t  no_of_values
    ); """
ps3000.make_symbol("_get_values", "ps3000_get_values", c_int32,
                   [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_int32], doc)

doc = """ void ps3000_release_stream_buffer
    (
        int16_t  handle
    ); """
ps3000.make_symbol("_release_stream_buffer", "ps3000_release_stream_buffer", None, [c_int16, ], doc)

doc = """ int32_t ps3000_get_times_and_values
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
ps3000.make_symbol("_get_times_and_values", "ps3000_get_times_and_values", c_int32,
                   [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_int16, c_int32], doc)

doc = """ int16_t ps3000_open_unit_async
    (
        void
    ); """
ps3000.make_symbol("_open_unit_async", "ps3000_open_unit_async", c_int16, [], doc)

doc = """ int16_t ps3000_open_unit_progress
    (
        int16_t *handle,
        int16_t *progress_percent
    ); """
ps3000.make_symbol("_open_unit_progress", "ps3000_open_unit_progress", c_int16, [c_void_p, c_void_p], doc)

doc = """ int16_t ps3000_streaming_ns_get_interval_stateless
    (
        int16_t   handle,
        int16_t   nChannels,
        uint32_t *sample_interval
    ); """
ps3000.make_symbol("_streaming_ns_get_interval_stateless", "ps3000_streaming_ns_get_interval_stateless", c_int16,
                   [c_int16, c_int16, c_void_p], doc)

doc = """ int16_t ps3000_get_streaming_last_values
    (
        int16_t  handle,
        GetOverviewBuffersMaxMin
    ); """
ps3000.make_symbol("_get_streaming_last_values", "ps3000_get_streaming_last_values", c_int16, [c_int16, c_void_p], doc)

doc = """ int16_t ps3000_overview_buffer_status
    (
        int16_t  handle,
        int16_t *previous_buffer_overrun
    ); """
ps3000.make_symbol("_overview_buffer_status", "ps3000_overview_buffer_status", c_int16, [c_int16, c_void_p], doc)

doc = """ uint32_t ps3000_get_streaming_values
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
ps3000.make_symbol("_get_streaming_values", "ps3000_get_streaming_values", c_uint32,
                   [c_int16, c_void_p,
                    c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p,
                    c_void_p, c_void_p, c_void_p, c_uint32, c_uint32], doc)

doc = """ uint32_t ps3000_get_streaming_values_no_aggregation
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
ps3000.make_symbol("_get_streaming_values_no_aggregation", "ps3000_get_streaming_values_no_aggregation", c_uint32,
                   [c_int16, c_void_p,
                    c_void_p, c_void_p, c_void_p, c_void_p,
                    c_void_p, c_void_p, c_void_p, c_uint32], doc)

doc = """ int16_t ps3000_save_streaming_data
    (
        int16_t               handle,
        PS3000_CALLBACK_FUNC  lpCallbackFunc,
        int16_t              *dataBuffers,
        int16_t               dataBufferSize
    ); """
ps3000.make_symbol("_save_streaming_data", "ps3000_save_streaming_data", c_int16,
                   [c_int16, c_void_p, c_void_p, c_int16], doc)

doc = """ int16_t ps3000SetAdvTriggerChannelProperties
    (
        int16_t                            handle,
        PS3000_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                            nChannelProperties,
        int32_t                            autoTriggerMilliseconds
    ); """
ps3000.make_symbol("_SetAdvTriggerChannelProperties", "ps3000SetAdvTriggerChannelProperties", c_int16,
                   [c_int16, c_void_p, c_int16, c_int32], doc)

doc = """ int16_t ps3000SetAdvTriggerChannelConditions
    (
        int16_t                    handle,
        PS3000_TRIGGER_CONDITIONS *conditions,
        int16_t                    nConditions
    ); """
ps3000.make_symbol("_SetAdvTriggerChannelConditions", "ps3000SetAdvTriggerChannelConditions", c_int16,
                   [c_int16, c_void_p, c_int16], doc)

doc = """ int16_t ps3000SetAdvTriggerChannelDirections
    (
        int16_t                     handle,
        PS3000_THRESHOLD_DIRECTION  channelA,
        PS3000_THRESHOLD_DIRECTION  channelB,
        PS3000_THRESHOLD_DIRECTION  channelC,
        PS3000_THRESHOLD_DIRECTION  channelD,
        PS3000_THRESHOLD_DIRECTION  ext
    ); """
ps3000.make_symbol("_SetAdvTriggerChannelDirections", "ps3000SetAdvTriggerChannelDirections", c_int16,
                   [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32], doc)

doc = """ int16_t ps3000SetPulseWidthQualifier
    (
        int16_t                     handle,
        PS3000_PWQ_CONDITIONS      *conditions,
        int16_t                     nConditions,
        PS3000_THRESHOLD_DIRECTION  direction,
        uint32_t                    lower,
        uint32_t                    upper,
        PS3000_PULSE_WIDTH_TYPE     type
    ); """
ps3000.make_symbol("_SetPulseWidthQualifier", "ps3000SetPulseWidthQualifier", c_int16,
                   [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32], doc)

doc = """ int16_t ps3000SetAdvTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay,
        float     preTriggerDelay
    ); """
ps3000.make_symbol("_SetAdvTriggerDelay", "ps3000SetAdvTriggerDelay", c_int16, [c_int16, c_uint32, c_float], doc)

doc = """ int16_t ps3000PingUnit
    (
        int16_t  handle
    ); """
ps3000.make_symbol("_PingUnit", "ps3000PingUnit", c_int16, [c_int16, ], doc)

ps3000.PICO_INFO = {k: v for k, v in ps3000.PICO_INFO.items() if v <= 0x00000005}
ps3000.PICO_INFO["PICO_ERROR_CODE"] = 0x00000006
