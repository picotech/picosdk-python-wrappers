#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the pl1000.h C header
file for PicoLog 1000 Series datalogger using the pl1000 driver API functions.
"""

from ctypes import *
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.library import Library
from picosdk.constants import make_enum

class Pl1000lib(Library):
    def __init__(self):
        super(Pl1000lib, self).__init__("pl1000")
		
pl1000 = Pl1000lib()

def _pl1000Inputs():
    PL1000_CHANNEL_1 = 1
	PL1000_CHANNEL_2 = 2
	PL1000_CHANNEL_3 = 3
	PL1000_CHANNEL_4 = 4
	PL1000_CHANNEL_5 = 5
	PL1000_CHANNEL_6 = 6
	PL1000_CHANNEL_7 = 7
	PL1000_CHANNEL_8 = 8
	PL1000_CHANNEL_9 = 9
	PL1000_CHANNEL_10 = 10
	PL1000_CHANNEL_11 = 11
	PL1000_CHANNEL_12 = 12
	PL1000_CHANNEL_13 = 13
	PL1000_CHANNEL_14 = 14
	PL1000_CHANNEL_15 = 15
	PL1000_CHANNEL_16 = 16
	PL1000_MAX_CHANNEL = PL1000_CHANNEL_16
	
	return {k.upper(): v for k, v in locals().items() if k.startswith("PL1000")}
	
pl1000.PL1000Inputs = _pl1000Inputs()

pl1000.PL1000DO_Channel = make_enum([
    'PL1000_DO_CHANNEL_0',
	'PL1000_DO_CHANNEL_1',
	'PL1000_DO_CHANNEL_2',
	'PL1000_DO_CHANNEL_3',
	'PL1000_DO_CHANNEL_MAX',
])

pl1000.PL1000OpenProgress = {
    'PL1000_OPEN_PROGRESS_FAIL' : -1,
	'PL1000_OPEN_PROGRESS_PENDING': 0,
	'PL1000_OPEN_PROGRESS_COMPLETE' : 1,
}