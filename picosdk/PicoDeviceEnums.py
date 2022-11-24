#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the enumerations from the PicoDeviceEnums.h C header
file for use with PicoScope 6000 A Series oscilloscopes using the ps6000a driver API
functions.
"""

from ctypes import *
from picosdk.constants import make_enum
from picosdk.library import Library

class PicoEnumlib(Library):
    def __init__(self):
        super(PicoEnumlib, self).__init__("ps6000a")


picoEnum  = PicoEnumlib()

def _define_ratio_mode():
    PICO_RATIO_MODE_AGGREGATE = 1
    PICO_RATIO_MODE_DECIMATE = 2
    PICO_RATIO_MODE_AVERAGE = 4
    PICO_RATIO_MODE_DISTRIBUTION = 8
    PICO_RATIO_MODE_SUM = 16
    PICO_RATIO_MODE_TRIGGER_DATA_FOR_TIME_CALCUATION = 0x10000000
    PICO_RATIO_MODE_SEGMENT_HEADER = 0x20000000
    PICO_RATIO_MODE_TRIGGER = 0x40000000
    PICO_RATIO_MODE_RAW = 0x80000000
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}
    
picoEnum.PICO_RATIO_MODE = _define_ratio_mode()

def _define_channel():
    PICO_CHANNEL_A = 0
    PICO_CHANNEL_B = 1
    PICO_CHANNEL_C = 2
    PICO_CHANNEL_D = 3
    PICO_CHANNEL_E = 4
    PICO_CHANNEL_F = 5
    PICO_CHANNEL_G = 6
    PICO_CHANNEL_H = 7
    PICO_PORT0 = 128
    PICO_PORT1 = 129
    PICO_PORT2 = 130
    PICO_PORT3 = 131
    PICO_EXTERNAL = 1000
    PICO_TRIGGER_AUX = 1001
    PICO_PULSE_WIDTH_SOURCE = 0x10000000
    PICO_DIGITAL_SOURCE = 0x10000001
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}
    
picoEnum.PICO_CHANNEL = _define_channel()

def _define_channel_flags():
    PICO_CHANNEL_A_FLAGS = 1
    PICO_CHANNEL_B_FLAGS = 2
    PICO_CHANNEL_C_FLAGS = 4
    PICO_CHANNEL_D_FLAGS = 8
    PICO_CHANNEL_E_FLAGS = 16
    PICO_CHANNEL_F_FLAGS = 32
    PICO_CHANNEL_G_FLAGS = 64
    PICO_CHANNEL_H_FLAGS = 128
    PICO_PORT0_FLAGS = 65536
    PICO_PORT1_FLAGS = 131072
    PICO_PORT2_FLAGS = 262144
    PICO_PORT3_FLAGS = 524288
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}

picoEnum.PICO_CHANNEL_FLAGS = _define_channel_flags()

picoEnum.PICO_PORT_DIGITAL_CHANNEL = make_enum([
    "PICO_PORT_DIGITAL_CHANNEL0",
    "PICO_PORT_DIGITAL_CHANNEL1",
    "PICO_PORT_DIGITAL_CHANNEL2",
    "PICO_PORT_DIGITAL_CHANNEL3",
    "PICO_PORT_DIGITAL_CHANNEL4"
    "PICO_PORT_DIGITAL_CHANNEL5",
    "PICO_PORT_DIGITAL_CHANNEL6",
    "PICO_PORT_DIGITAL_CHANNEL7",
    ])
    
picoEnum.PICO_DATA_TYPE = make_enum([
    "PICO_INT8_T",
    "PICO_INT16_T",
    "PICO_INT32_T",
    "PICO_UINT32_T",
    "PICO_INT64_T",
    ])

def _define_coupling():
    PICO_AC = 0
    PICO_DC = 1
    PICO_DC_50OHM = 50
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}

picoEnum.PICO_COUPLING = _define_coupling()

# PicoBandwitdthLimiterFlags
# needs implementing still

def _define_bandwidth_limiter():
    PICO_BW_FULL = 0
    PICO_BW_100KHZ = 100000
    PICO_BW_20KHZ = 20000
    PICO_BW_1MHZ = 1000000
    PICO_BW_20MHZ = 20000000
    PICO_BW_25MHZ = 25000000
    PICO_BW_50MHZ = 50000000
    PICO_BW_250MHZ = 250000000
    PICO_BW_500MHZ = 500000000
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}
    
picoEnum.PICO_BANDWIDTH_LIMITER = _define_bandwidth_limiter()

picoEnum.PICO_PULSE_WIDTH_TYPE = make_enum([
    "PICO_PW_TYPE_NONE",
    "PICO_PW_TYPE_LESS_THAN",
    "PICO_PW_TYPE_GREATER_THAN",
    "PICO_PW_IN_RANGE",
    "PICO_PW_TYPE_OUT_OF_RANGE"
    ])
    
picoEnum.PICO_SWEEP_TYPE = make_enum([
    "PICO_UP",
    "PICO_DOWN",
    "PICO_UPDOWN",
    "PICO_DOWNUP"
    ])
    
def _define_wave_type():
    PICO_SINE = 0x00000011
    PICO_SQUARE = 0x00000012
    PICO_TRIANGLE = 0x00000013
    PICO_RAMP_UP = 0x00000014
    PICO_RAMP_DOWN = 0x00000015
    PICO_SINC = 0x00000016
    PICO_GAUSSIAN = 0x00000017
    PICO_HALF_SINE = 0x00000018
    PICO_DC_VOLTAGE = 0x00000400
    PICO_PWM = 0x00001000
    PICO_WHITENOISE = 0x00002001
    PICO_PRBS = 0x00002002
    PICO_ARBITRARY = 0x10000000
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}

picoEnum.PICO_WAVE_TYPE = _define_wave_type()

picoEnum.PICO_SIGGEN_TRIG_TYPE = make_enum([
    "PICO_SIGGEN_RISING",
    "PICO_SIGGEN_FALLING",
    "PICO_SIGGEN_GATE_HIGH",
    "PICO_SIGGEN_GATE_LOW"
    ])
    
picoEnum.PICO_SIGGEN_TRIG_SOURCE = make_enum([
    "PICO_SIGGEN_NONE",
    "PICO_SIGGEN_SCOPE_TRIG",
    "PICO_SGGEN_AUX_IN",
    "PICO_SIGGEN_EXT_IN",
    "PICO_SIGGEN_SOFT_TRIG",
    "PICO_SIGGEN_TRIGGER_RAW"
    ])
    
picoEnum.PICO_SIGGEN_FILTER_STATE = make_enum([
    "PICO_SIGGEN_FILTER_AUTO",
    "PICO_SIGGEN_FILTER_OFF",
    "PICO_SIGGEN_FILTER_ON"
    ])
    
picoEnum.PICO_SIGGEN_PARAMETER = make_enum([
    "PICO_SIGGEN_PARAM_OUTPUT_VOLTS",
    "PICO_SIGGEN_PARAM_SAMPLE",
    "PICO_SIGGEN_BUFFER_LENGTH"
    ])
    
picoEnum.PICO_TIME_UNITS = make_enum([
    "PICO_FS",
    "PICO_PS",
    "PICO_NS",
    "PICO_US",
    "PICO_MS",
    "PICO_S"
    ])

def _define_threshold_direction():
    PICO_ABOVE = PICO_INSIDE = 0
    PICO_BELOW = PICO_OUTSIDE = 1
    PICO_RISING = PICO_ENTER = PICO_NONE = 2 
    PICO_FALLING = PICO_EXIT = 3
    PICO_RISING_OR_FALLING = PICO_ENTER_OR_EXIT = 4
    PICO_ABOVE_LOWER = 5
    PICO_BELOW_LOWER = 6
    PICO_RISING_LOWER = 7
    PICO_FALLING_LOWER = 8
    PICO_POSITIVE_RUNT = 9
    PICO_NEGATIVE_RUNT = 10
    PICO_LOGIC_LOWER = 1000
    PICO_LOGIC_UPPER = 1001
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}
    
picoEnum.PICO_THRESHOLD_DIRECTION = _define_threshold_direction()

picoEnum.PICO_THRESHOLD_MODE = make_enum([
    "PICO_LEVEL",
    "PICO_WINDOW"
    ])
    
picoEnum.PICO_ETS_MODE = make_enum([
    "PICO_ETS_OFF",
    "PICO_WINDOW",
    ])
    
picoEnum.PICO_INDEX_MODE = make_enum([
    "PICO_SINGLE",
    "PICO_DUAL",
    "PICO_QUAD"
    ])
    
def _define_action():
    PICO_CLEAR_ALL = 0x00000001
    PICO_ADD = 0x00000002
    PICO_CLEAR_THIS_DATA_BUFFER = 0x00001000
    PICO_CLEAR_WAVEFORM_DATA_BUFFERS = 0x00002000
    PICO_CLEAR_WAVEFORM_READ_DATA_BUFFERS = 0x00004000
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}
    
picoEnum.PICO_ACTION = _define_action()

picoEnum.PICO_TRIGGER_STATE = make_enum([
    "PICO_CONDITION_DONT_CARE",
    "PICO_CONDITION_TRUE",
    "PICO_CONDITION_FALSE"
    ])
    
def _define_resolution():
    PICO_DR_8BIT = 0
    PICO_DR_12BIT = 1
    PICO_DR_14BIT = 2
    PICO_DR_15BIT = 3
    PICO_DR_16BIT = 4
    PICO_DR_10BIT = 10
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}
    
picoEnum.PICO_DEVICE_RESOLUTION = _define_resolution()

picoEnum.PICO_READ_SELECTION = make_enum([
    "PICO_READSELECTION_NONE",
    "PICO_TRIGGER_READ",
    "PICO_DATA_READ1",
    "PICO_DATA_READ2",
    "PICO_DATA_READ3"
    ])

picoEnum.PICO_TRIM_ACTION = make_enum([
    "PICO_OLDEST",
    "PICO_RECENT"
    ])

picoEnum.PICO_DIGITAL_PORT_HYSTERESIS = make_enum([
    "PICO_VERY_HIGH_400MV",
    "PICO_HIGH_200MV",
    "PICO_NORMAL_100MV",
    "PICO_LOW_50MV"
    ])
    
picoEnum.PICO_DIGITAL_DIRECTION = make_enum([
    "PICO_DIGITAL_DONT_CARE",
    "PICO_DIGITAL_DIRECTION_LOW",
    "PICO_DIGITAL_DIRECTION_HIGH",
    "PICO_DIGITAL_DIRECTION_RISING",
    "PICO_DIGITAL_DIRECTION_FALLING",
    "PICO_DIGITAL_DIRECTION_RISING_OR_FALLING",
    "PICO_DIGITAL_DIRECTION_MAX_DIRECTION"
    ])
    
def _define_conditions_info():
    PICO_CLEAR_CONDITIONS = 0x00000001
    PICO_ADD_CONDITIONS = 0x00000002
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}
    
picoEnum.PICO_CONDITIONS_INFO = _define_conditions_info()

picoEnum.PICO_CLOCK_REFERENCE = make_enum([
    "PICO_INTERNAL_REF",
    "PICO_EXTERNAL_REF"
    ])
    
picoEnum.PICO_TRIGGER_WITHIN_PRE_TRIGGER = make_enum([
    "PICO_DISABLE",
    "PICO_ARM"
    ])
    
picoEnum.PICO_TEMPERATURE_REFERENCE = make_enum([
    "PICO_TEMPERATURE_UNINITIALISED",
    "PICO_TEMPERATURE_NORMAL",
    "PICO_TEMPERATURE_WARNING",
    "PICO_TEMPERATURE_CRITICAL",
    "PICO_TEMPERATURE_REFERENCE"
    ])
    
def _define_digital_port():
    Pico_DIGITAL_PORT_NONE = 0
    PICO_DIGITAL_PORT_MSO_POD = 1000
    PICO_DIGITAL_PORT_UNKNOWN_DEVICE = -2
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("PICO")}
    
picoEnum.PICO_DIGITAL_PORT = _define_digital_port