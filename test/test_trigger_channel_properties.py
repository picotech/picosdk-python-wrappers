import unittest
from ctypes import Structure, c_int16, c_int32, c_uint16, c_uint32, c_void_p, byref
from picosdk.library import Library
from picosdk.device import Device


class DummyDevice(Device):
    def __init__(self, driver):
        super(DummyDevice, self).__init__(driver, 42)


class DummyDriver(Library):
    def __init__(self):
        self.name = 'ps3000a'
        # Emulate necessary structures and definitions on Driver/Library
        self.PICO_STATUS = {'PICO_OK': 0}
        self.PICO_CHANNEL = {'A': 0}
        self.PS3000A_THRESHOLD_DIRECTION = {
            'PS3000A_NONE': 2,
            'PS3000A_RISING': 2,
            'PS3000A_FALLING': 3
        }
        self.PS3000A_THRESHOLD_MODE = {
            'PS3000A_LEVEL': 0,
            'PS3000A_WINDOW': 1
        }

        class PS3000A_TRIGGER_CHANNEL_PROPERTIES(Structure):
            _pack_ = 1
            _fields_ = [("thresholdUpper", c_int16),
                        ("thresholdUpperHysteresis", c_uint16),
                        ("thresholdLower", c_int16),
                        ("thresholdLowerHysteresis", c_uint16),
                        ("channel", c_uint32),
                        ("thresholdMode", c_uint32)]
        self.PS3000A_TRIGGER_CHANNEL_PROPERTIES = PS3000A_TRIGGER_CHANNEL_PROPERTIES

        self.last_call_args = None

        # Emulate a C function registered on the driver
        def dummy_c_func(handle, channel_properties, n_properties, aux_enable, auto_trigger_ms):
            self.last_call_args = (handle, channel_properties, n_properties, aux_enable, auto_trigger_ms)
            return 0  # PICO_OK

        dummy_c_func.argtypes = [c_int16, c_void_p, c_int16, c_int16, c_int32]
        dummy_c_func.restype = c_uint32

        self._set_trigger_channel_properties = dummy_c_func

    def _convert_args(self, func, args):
        converted = []
        for arg, argtype in zip(args, func.argtypes):
            if isinstance(arg, Structure):
                self.last_properties = arg
            if argtype == c_void_p and arg is not None:
                converted.append(byref(arg))
            elif arg is not None:
                converted.append(argtype(arg))
            else:
                converted.append(None)
        return tuple(converted)


class TriggerChannelPropertiesTest(unittest.TestCase):
    def test_set_trigger_channel_properties_success(self):
        driver = DummyDriver()
        device = DummyDevice(driver)

        driver.set_trigger_channel_properties(
            device=device,
            threshold_upper=1000,
            threshold_upper_hysteresis=100,
            threshold_lower=-1000,
            threshold_lower_hysteresis=50,
            channel='A',
            threshold_mode='LEVEL',
            aux_output_enable=False,
            auto_trigger_milliseconds=500
        )

        # Verify the C function was called with correct arguments
        self.assertIsNotNone(driver.last_call_args)
        handle, channel_properties_ref, n_properties, aux_enable, auto_trigger_ms = driver.last_call_args

        self.assertEqual(handle.value, 42)
        self.assertEqual(n_properties.value, 1)
        self.assertEqual(aux_enable.value, 0)
        self.assertEqual(auto_trigger_ms.value, 500)

        # Verify the structure fields directly
        props = driver.last_properties
        self.assertEqual(props.thresholdUpper, 1000)
        self.assertEqual(props.thresholdUpperHysteresis, 100)
        self.assertEqual(props.thresholdLower, -1000)
        self.assertEqual(props.thresholdLowerHysteresis, 50)
        self.assertEqual(props.channel, 0)
        self.assertEqual(props.thresholdMode, 0)  # LEVEL mapped to 0

    def test_set_null_trigger_calls_driver_with_device(self):
        driver = DummyDriver()
        device = DummyDevice(driver)

        called_device = None
        def mock_set_null_trigger(device, channel="A"):
            nonlocal called_device
            called_device = device

        driver.set_null_trigger = mock_set_null_trigger
        device.set_null_trigger()

        self.assertEqual(called_device, device)

