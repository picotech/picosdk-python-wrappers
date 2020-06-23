# picosdk-python-wrappers

Welcome to the PicoSDK for Python. It allows you to control PicoScope devices in your own Python programs.

## Getting started

To use this code you will need to install the PicoSDK C libraries.

### Microsoft Windows

Please visit [our Downloads page](https://www.picotech.com/downloads) to download the 32-bit or 64-bit PicoSDK C Libraries for Windows. 
Please take care to match the "bitness" of your python to the PicoSDK.

### Linux

Follow the instructions from our [Linux Software & Drivers for Oscilloscopes and Data Loggers page](https://www.picotech.com/downloads/linux) 
to install the required driver packages for your product.

### macOS

macOS users should install PicoScope Beta for macOS, and then may find this [forum post](https://www.picotech.com/support/topic22221.html) helpful for installing the C 
libraries.

## Installing the python driver bindings

A `distutils` installer is provided. After you have installed the PicoSDK
driver package (see above), the Python installer can be used as follows:

    python setup.py install

On macOS and Linux you will either need to use `sudo` with this command, to
install into the system folders, or to install for the current user only you
can use:

    python setup.py install --user

Within python, the library for `import` is called `picosdk`.

## Compatibility

This code is written to be compatible with both python 2.7 and python 3 (any version).

If you find a compatibility problem please raise an [Issue](https://www.picotech.com/tech-support), listing all the versions you can find (python, numpy, 
picosdk commit hash, etc.) and your error message(s).

## C interface

You can access C driver functions directly (ctypes calls) by their original C name, following the [Programmer's
Guides](https://github.com/picotech/picosdk-python-wrappers#programmers-guides) exactly. Examples are provided in the folders like `psX000[a]Examples/`.

### Programmer's Guides

You can download Programmer's Guides providing a description of the API functions for the relevant PicoScope or 
PicoLog driver from our [Documentation page](https://www.picotech.com/library/documentation).

## Python interface

We are in the process of adding Pythonic wrappers around the C functions. If we haven't got to your feature yet or your device is listed as one of the [unsupported models](https://github.com/picotech/picosdk-python-wrappers#unsupported-models),
let us know that you're waiting in an [Issue](https://www.picotech.com/tech-support)

### Unsupported models

The following drivers and devices are not yet supported:

* `plcm3` - PicoLog CM3 Current Data Logger
* `ps3000` - PicoScope 3204, 3205, 3206, 3223, 3224, 3423 & 3423
* `usbpt104` - PT-104 Platinum Resistance Data Logger

### Dependencies

As well as depending on the C libraries, the Pythonic wrappers use some python libraries like `numpy`. Many of the
examples scripts also use the `matplotlib` plotting library. You can install these dependencies with pip as follows:

    pip install -r requirements.txt
    pip install -r requirements-for-examples.txt

### Driver-agnostic examples

The `anyScopeExamples` folder contains examples in pure python which do the same thing as the C-style examples, but
in a driver-generic way.

### Python Classes

#### Library

`picosdk.library.Library` contains a base class for each of the driver classes. It does the job of translating python
types into C ones, and back again, and some unit conversions to get rid of nano, micro and milli-style prefixes. It also
handles any differences in programming API between PicoScope driver versions.

#### Device

`picosdk.device.Device` contains the concrete class which represents a PicoScope with a valid handle. It caches some
information about the device state, like the currently selected voltage ranges of the channels.

It is implemented in terms of the Library class' public interface, and deals almost entirely with python types. The
main exception is its handling of numpy arrays - it (knowing the voltage ranges) is responsible for converting the raw
ADC counts that the driver uses for amplitude into physical units.

## Testing this code

Check which device driver your device uses, and check the constants at the top of test/test_helpers.py to enable the 
relevant drivers for connected-device tests. (most tests use this).

To check which driver your device uses, you can use `picosdk.discover`:

    from picosdk.discover import find_all_units
    
    scopes = find_all_units()
    
    for scope in scopes:
        print(scope.info)
        scope.close()

You should then configure test/test_helpers.py's list of connected devices, so it can run all the tests we have
on your device.

To run the unit tests, you will need to install nose (e.g. `pip install nose`.) Then, run `nosetests` in the root of 
the repo. 

## Obtaining support

Please visit our [Support page](https://www.picotech.com/tech-support) to contact us directly or visit our [Test and Measurement Forum](https://www.picotech.com/support/forum17.html) to post questions.

## Copyright and licensing

See [LICENSE.md](LICENSE.md) for license terms. 

*PicoScope*, *PicoLog* and *PicoSDK* are registered trademarks of Pico Technology Ltd. 

*Windows* is a registered trademark of Microsoft Corporation. 

*macOS* is a registered trademark of Apple Inc. 

*Linux* is the registered trademark of Linus Torvalds in the U.S. and other countries.

Copyright © 2018-2019 Pico Technology Ltd. All rights reserved. 
