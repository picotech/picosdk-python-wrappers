## Python interface

The library class's public methods (ones not starting with an underscore) form a sanitised Python interface to the
picosdk driver libraries. For instance, if you have multiple picotech devices connected, and you want to locate and open
the only 2205A:

    from picosdk.ps2000 import ps2000

    available_devices = ps2000.list_units()

    my_2205A_info = [d for d in available_devices if d.variant == "2205A"][0]

    assert my_2205A_info.driver == ps2000

    my_2205A = ps2000.open_unit(my_2205A_info.serial)

    # see the device module for the interface of the device class.

Calls in each driver have been abstracted into python-friendly methods here, so have a look below to see what your
device's driver functions have been named (and what python parameters they accept.)

## C interface

You can also access C driver functions directly (ctypes calls) by their original C name, following the programming
guides exactly:

    from __future__ import print_function
    from ctypes import c_int16, create_string_buffer
    from picosdk.ps2000 import ps2000

    chandle = ps2000.ps2000_open_unit()

    if chandle.value == -1:
        raise Exception("Oscilloscope failed to open")
    elif chandle.value == 0:
        raise Exception("No device found")

    try:
        handle = chandle.value

        PS2000_BATCH_AND_SERIAL = c_int16(4)
        STRING_SIZE = 255
        cinfo = create_string_buffer("\0", STRING_SIZE)
        cinfo_len = ps2000.ps2000_get_unit_info(c_int16(handle), cinfo, c_int16(STRING_SIZE), PS2000_BATCH_AND_SERIAL)
        if cinfo_len.value <= 0:
            raise Exception("parameter out of range")

        serial = info.value[:cinfo_len.value]

        print("found ps2000 device with serial %s" % serial)

    finally:
        ps2000.ps2000_close_unit(c_int16(handle))