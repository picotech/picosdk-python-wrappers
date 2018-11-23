#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
from __future__ import division
import numpy as np
import ctypes
from picosdk.constants import PICO_STATUS, PICO_STATUS_LOOKUP


class PicoSDKCtypesError(Exception):
    pass


def adc2mV(bufferADC, range, maxADC):
    """ 
        adc2mc(
                c_short_Array           bufferADC
                int                     range
                c_int32                 maxADC
                )
               
        Takes a buffer of raw adc count values and converts it into millivolts
    """

    channelInputRanges = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]
    vRange = channelInputRanges[range]
    bufferV = [(x * vRange) / maxADC.value for x in bufferADC]

    return bufferV

def mV2adc(volts, range, maxADC):
    """
        mV2adc(
                float                   volts
                int                     range
                c_int32                 maxADC
                )
        Takes a voltage value and converts it into adc counts
    """
    channelInputRanges = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]
    vRange = channelInputRanges[range]
    adcValue = round((volts * maxADC.value)/vRange)

    return adcValue



def splitMSODataPort0(cmaxSamples, bufferMax):
    """
        splitMSODataPort0(
                        c_int32         cmaxSamples
                        c_int16 array   bufferMax
                        )
    """
    # Makes an array for each digital channel
    bufferMaxBinaryD0 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD1 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD2 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD3 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD4 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD7 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD5 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD6 = np.chararray((cmaxSamples.value, 1))
    
    # Changes the data from int type to a binary type and then separates the data for each digital channel
    for i in range(0, cmaxSamples.value):
        MSOData = bufferMax[i]
        binaryMSOData = bin(MSOData)
        binaryMSOData = binaryMSOData[2:]
        binaryMSOData = binaryMSOData.zfill(8)
        bufferMaxBinaryD0[i] = binaryMSOData[7]
        bufferMaxBinaryD1[i] = binaryMSOData[6]
        bufferMaxBinaryD2[i] = binaryMSOData[5]
        bufferMaxBinaryD3[i] = binaryMSOData[4]
        bufferMaxBinaryD4[i] = binaryMSOData[3]
        bufferMaxBinaryD5[i] = binaryMSOData[2]
        bufferMaxBinaryD6[i] = binaryMSOData[1]
        bufferMaxBinaryD7[i] = binaryMSOData[0]

    return bufferMaxBinaryD0, bufferMaxBinaryD1, bufferMaxBinaryD2, bufferMaxBinaryD3, bufferMaxBinaryD4, bufferMaxBinaryD5, bufferMaxBinaryD6, bufferMaxBinaryD7

def splitMSODataPort1(cmaxSamples, bufferMax):
    """
        splitMSODataPort1(
                        c_int32         cmaxSamples
                        c_int16 array   bufferMax
                        )
    """
    # Makes an array for each digital channel
    bufferMaxBinaryD8 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD9 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD10 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD11 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD12 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD13 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD14 = np.chararray((cmaxSamples.value, 1))
    bufferMaxBinaryD15 = np.chararray((cmaxSamples.value, 1))
    
    # Changes the data from int type to a binary type and then separates the data for each digital channel
    for i in range(0, cmaxSamples.value):
        MSOData = bufferMax[i]
        binaryMSOData = bin(MSOData)
        binaryMSOData = binaryMSOData[2:]
        binaryMSOData = binaryMSOData.zfill(8)
        bufferMaxBinaryD8[i] = binaryMSOData[7]
        bufferMaxBinaryD9[i] = binaryMSOData[6]
        bufferMaxBinaryD10[i] = binaryMSOData[5]
        bufferMaxBinaryD11[i] = binaryMSOData[4]
        bufferMaxBinaryD12[i] = binaryMSOData[3]
        bufferMaxBinaryD13[i] = binaryMSOData[2]
        bufferMaxBinaryD14[i] = binaryMSOData[1]
        bufferMaxBinaryD15[i] = binaryMSOData[0]

    return bufferMaxBinaryD8, bufferMaxBinaryD9, bufferMaxBinaryD10, bufferMaxBinaryD11, bufferMaxBinaryD12, bufferMaxBinaryD13, bufferMaxBinaryD14, bufferMaxBinaryD15

def splitMSOData(cmaxSamples, data):
    """
    # This implementation will work on either channel in the same way as the Port0 and Port1 methods above.
        splitMSOData(
                        c_int32         cmaxSamples
                        c_int16 array   data
                        )
    """
    # Makes an array for each digital channel
    bufferBinaryDj = (
        np.chararray((cmaxSamples.value, 1)),
        np.chararray((cmaxSamples.value, 1)),
        np.chararray((cmaxSamples.value, 1)),
        np.chararray((cmaxSamples.value, 1)),
        np.chararray((cmaxSamples.value, 1)),
        np.chararray((cmaxSamples.value, 1)),
        np.chararray((cmaxSamples.value, 1)),
        np.chararray((cmaxSamples.value, 1)),
    )
    # Splits out the individual bits from the port into the binary values for each channel/pin.
    for i in range(cmaxSamples.value):
        for j in range(7):
            bufferBinaryDj[j][i] = 1 if (data[i] & 1 << (7-j)) else 0

    return bufferBinaryDj

def assert_pico_ok(status):
    """
        assert_pico_ok(
                        status
                       )
    """
    # checks for PICO_OK status return
    if status != PICO_STATUS['PICO_OK']:
        raise PicoSDKCtypesError("PicoSDK returned '{}'".format(PICO_STATUS_LOOKUP[status]))


def assert_pico2000_ok(status):
    """
        assert_pico_ok(
                        status
                       )
    """
    # checks for PICO_OK status return
    if status > 0:
        errorCheck = True
    else:
        errorCheck = False
        raise PicoSDKCtypesError("Unsuccessful API call")
