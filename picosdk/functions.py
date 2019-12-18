#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
from __future__ import division
import numpy as np
from picosdk.constants import PICO_STATUS, PICO_STATUS_LOOKUP
from picosdk.errors import PicoSDKCtypesError


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
	
def adc2mVpl1000(bufferADC, range, maxADC):
	"""
		adc2mVpl1000(
						c_short_Array		bufferADC,
						int 				range,
						c_int32				maxADC
						)
		
		Takes a buffer of raw adc count values and converts it into millvolts
	"""
	
	bufferV = [(x * range) / maxADC.value for x in bufferADC]
	
	return bufferV

def mV2adc(millivolts, range, maxADC):
    """
        mV2adc(
                float                   millivolts
				int                     range
                c_int32                 maxADC
                )
        Takes a voltage value and converts it into adc counts
    """
    channelInputRanges = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]
    vRange = channelInputRanges[range]
    adcValue = round((millivolts * maxADC.value)/vRange)

    return adcValue

def mV2adcpl1000(millivolts, range, maxADC):
	"""
		mV2adc(
				float				millivolts,
				int					range,
				c_int32				maxADC
				)
		Takes a voltage value and converts it to adc counts
	"""
	adcValue = round((millivolts * maxADC.value)/range)
	
	return adcValue


def splitMSOData(dataLength, data):
    """
    This method converts an array of values for a ditial port into the binary equivalent, splitting the bits by
    digital channel.

    Returns a set of 8 variables, each of which corresponds to the binary data values over time of the different
    digital channels from the lowest significant bit to the most significant bit. For PORT0 this will be in the order
    (D0, D1, D2, ... D7) and for PORT1 this will be (D8, D9, D10, ... D15).

        splitMSOData(
                        c_int32         dataLength
                        c_int16 array   data
                        )
    """
    # Makes an array for each digital channel
    binaryBufferD0 = np.chararray((dataLength.value, 1))
    binaryBufferD1 = np.chararray((dataLength.value, 1))
    binaryBufferD2 = np.chararray((dataLength.value, 1))
    binaryBufferD3 = np.chararray((dataLength.value, 1))
    binaryBufferD4 = np.chararray((dataLength.value, 1))
    binaryBufferD7 = np.chararray((dataLength.value, 1))
    binaryBufferD5 = np.chararray((dataLength.value, 1))
    binaryBufferD6 = np.chararray((dataLength.value, 1))
    
    # Changes the data from int type to a binary type and then separates the data for each digital channel
    for i in range(0, dataLength.value):
        MSOData = data[i]
        binaryMSOData = bin(MSOData)
        binaryMSOData = binaryMSOData[2:]
        binaryMSOData = binaryMSOData.zfill(8)
        binaryBufferD0[i] = binaryMSOData[7]
        binaryBufferD1[i] = binaryMSOData[6]
        binaryBufferD2[i] = binaryMSOData[5]
        binaryBufferD3[i] = binaryMSOData[4]
        binaryBufferD4[i] = binaryMSOData[3]
        binaryBufferD5[i] = binaryMSOData[2]
        binaryBufferD6[i] = binaryMSOData[1]
        binaryBufferD7[i] = binaryMSOData[0]

    return binaryBufferD0, \
           binaryBufferD1, \
           binaryBufferD2, \
           binaryBufferD3, \
           binaryBufferD4, \
           binaryBufferD5, \
           binaryBufferD6, \
           binaryBufferD7


def splitMSODataFast(dataLength, data):
    """
    # This implementation will work on either channel in the same way as the splitMSOData method above, albeit in a
    more efficient manner.

    Returns a tuple of 8 arrays, each of which is the values over time of a different digital channel.
    The tuple contains the channels in order (D7, D6, D5, ... D0) or equivalently (D15, D14, D13, ... D8).

        splitMSODataFast(
                        c_int32         dataLength
                        c_int16 array   data
                        )
    """
    # Makes an array for each digital channel
    bufferBinaryDj = (
        np.chararray(dataLength.value),
        np.chararray(dataLength.value),
        np.chararray(dataLength.value),
        np.chararray(dataLength.value),
        np.chararray(dataLength.value),
        np.chararray(dataLength.value),
        np.chararray(dataLength.value),
        np.chararray(dataLength.value),
    )
    # Splits out the individual bits from the port into the binary values for each digital channel/pin.
    for i in range(dataLength.value):
        for j in range(8):
            bufferBinaryDj[j][i] = 1 if (data[i] & (1 << (7-j))) else 0

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
