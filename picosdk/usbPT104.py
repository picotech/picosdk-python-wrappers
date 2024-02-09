#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the usbPT104Api.h C header
file for Pico USB PT-104 datalogger using the usb PT104 driver API functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.constants import make_enum

class usbPT104lib(Library):
    def __init__(self):
        super(usbPT104lib, self).__init__("usbPt104")


usbPt104 = usbPT104lib()

usbPt104.PT104_CHANNELS = {
    'USBPT104_CHANNEL_1' : 1,
    'USBPT104_CHANNEL_2' : 2,
    'USBPT104_CHANNEL_3' : 3,
    'USBPT104_CHANNEL_4' : 4,
    'USBPT104_CHANNEL_5' : 5,
    'USBPT104_CHANNEL_6' : 6,
    'USBPT104_CHANNEL_7' : 7,
    'USBPT104_CHANNEL_8' : 8,
    'USBPT104_MAX_CHANNELS' : 8
}

usbPt104.PT104_DATA_TYPE = make_enum([
    'USBPT104_OFF',
    'USBPT104_PT100',
    'USBPT104_PT1000',
    'USBPT104_RESISTANCE_TO_375R',
    'USBPT104_RESISTANCE_TO_10K',
    'USBPT104_DIFFERENTIAL_TO_115MV',
    'USBPT104_DIFFERENTIAL_TO_2500MV',
    'USBPT104_SINGLE_ENDED_TO_115MV',
    'USBPT104_SINGLE_ENDED_TO_2500MV',
    'USBPT104_MAX_DATA_TYPES'
])

usbPt104.IP_DETAILS_TYPE = make_enum([
    'IDT_GET'
    'IDT_SET'
])

def _define_communication_type():
    CT_USB = 0x00000001
    CT_ETHERNET = 0x00000002
    CT_ALL = 0xFFFFFFFF
    
    return {k.upper(): v for k, v in locals().items() if k.startswith("CT")}
    
usbPt104.COMMUNICATION_TYPE = _define_communication_type

doc = """ PICO_STATUS UsbPt104CloseUnit
    (
        int16_t    handle
    ); """
usbPt104.make_symbol("_CloseUnit", "UsbPt104CloseUnit", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS UsbPt104Enumerate
    (
        int8_t    *details,
        uint32_t    *length,
        COMMUNICATION_TYPE    type
    ); """
usbPt104.make_symbol("_Enumerate", "UsbPt104Enumerate", c_uint32, [c_int8, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS UsbPt104GetUnitInfo
    (
        int16_t    handle,
        int8_t    *string,
        int16_t    stringLength,
        int16_t    *requiredSize,
        PICO_INFO    info
    ); """
usbPt104.make_symbol("_GetUnitInfo", "UsbPt104GetUnitInfo", c_uint32, [c_int16, c_void_p, c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS UsbPt104GetValue
    (
        int16_t    handle,
        USBPT104_CHANNELS    channel,
        int32_t    *value,
        int16_t    filtered
    ); """
usbPt104.make_symbol("_GetValue", "UsbPt104GetValue", c_uint32, [c_int16, c_uint32, c_void_p, c_int16], doc)

doc = """ PICO_STATUS UsbPt104IpDetails
    (
        int16_t    handle,
        int16_t    *enabled,
        int8_t    *ipaddress,
        uint16_t    *length,
        uint16_t    *listeningPort,
        IP_DETAILS_TYPE    type
    ); """
usbPt104.make_symbol("_IpDetails", "UsbPt104IpDetails", c_uint32, [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS UsbPt104OpenUnit
    (
        int16_t    *handle,
        int8_t    *serial
    ); """
usbPt104.make_symbol("_OpenUnit", "UsbPt104OpenUnit", c_uint32, [c_void_p, c_void_p], doc)

doc = """ PICO_STATUS UsbPt104OpenUnitViaIp
    (
        int16_t    *handle,
        int8_t    *serial,
        int8_t    *ipAddress
    ); """
usbPt104.make_symbol("_OpenUnitViaIp", "UsbPt104OpenUnitViaIp", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS UsbPt104SetChannel
    (
        int16_t    handle,
        USBPT104_CHANNELS    channel,
        USBPT104_DATA_TYPES    type,
        int16_t    noOfWires
    ); """
usbPt104.make_symbol("_SetChannel", "UsbPt104SetChannel", c_uint32, [c_int16, c_uint32, c_uint32, c_int16], doc)

doc = """ PICO_STATUS UsbPt104SetMains
    (
        int16_t    handle,
        uint16_t    sixty_hertz
    ); """
usbPt104.make_symbol("_SetMains", "UsbPt104SetMains", c_uint32, [c_int16, c_uint16], doc)
