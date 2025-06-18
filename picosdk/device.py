# coding=utf-8
#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Definition of the Device class, which provides access to SDK functions which require a device handle, including
capturing data and configuring the AWG.
"""
from __future__ import print_function
import collections
import numpy
import math
import time
from picosdk.errors import (DeviceCannotSegmentMemoryError, InvalidTimebaseError, ClosedDeviceError,
    NoChannelsEnabledError, NoValidTimebaseForOptionsError, FeatureNotSupportedError, ChannelNotEnabledError,
    InvalidRangeOfChannel)


DEFAULT_PROBE_ATTENUATION = {
    'A': 10,
    'B': 10,
    'C': 10,
    'D': 10,
    'E': 10,
    'F': 10,
    'G': 10,
    'H': 10,
}


def requires_open(error_message="This operation requires a device to be connected."):
    def check_open_decorator(method):
        def check_open_impl(self, *args, **kwargs):
            if not self.is_open:
                raise ClosedDeviceError(error_message)
            return method(self, *args, **kwargs)
        return check_open_impl
    return check_open_decorator


"""ChannelConfig: A type for specifying channel setup for capture (pass into Device.set_channel, or Device.capture_*)
name = The channel name as a string (e.g. 'A'.)
enabled = bool indicating whether the channel should be enabled or disabled.
coupling (optional) = 'AC' or 'DC', default is 'DC'.
range_peak (optional) = +/- max volts, the highest precision range which includes your value will be selected.
analog_offset (optional) = the meaning of 0 for this channel."""
ChannelConfig = collections.namedtuple('ChannelConfig', 'name enabled coupling range_peak analog_offset',
                                       defaults=['DC', float('inf'), None])


"""TimebaseOptions: A type for specifying timebase constraints (pass to Device.find_timebase or Device.capture_*)
All are optional. Please specify the options which matter to you:
  - the maximum time interval (if you want the fastest/most precise timebase you can get),
  - the number of samples in one buffer,
  - the minimum total collection time (if you want at least x.y seconds of uninterrupted capture data)
  - the oversample (if you want to sacrifice time precision for amplitude precision - see the programming guides.)"""
TimebaseOptions = collections.namedtuple('TimebaseOptions', ['max_time_interval',
                                                             'no_of_samples',
                                                             'min_collection_time',
                                                             'oversample'])
_TIMEBASE_OPTIONS_DEFAULTS = (None, None, None, 1)
TimebaseOptions.__new__.__defaults__ = _TIMEBASE_OPTIONS_DEFAULTS


class Device(object):
    """This object caches some information about the device state which cannot be queried from the driver. Please don't
    mix and match calls to this object with calls directly to the driver (or the ctypes wrapper), as this may cause
    unwanted behaviour (e.g. throwing an exception because no channels are enabled, when you enabled them yourself
    on the driver object.)"""
    def __init__(self, driver, handle):
        self._driver = driver
        self._handle = handle

        # if a channel is missing from here, it is disabled (or in an undefined state).
        self._max_adc = None
        self._buffers = {}
        self._max_samples = None
        self._channel_ranges = {}
        self._channel_offsets = {}
        self._enabled_sources = set()
        self._time_interval = None
        self._probe_attenuations = DEFAULT_PROBE_ATTENUATION

    @property
    def driver(self):
        return self._driver

    @property
    def handle(self):
        return self._handle

    @property
    def is_open(self):
        return self.handle is not None and self.handle > 0

    @property
    def max_adc(self):
        return self._max_adc

    @property
    def buffers(self):
        return self._buffers

    @property
    def max_samples(self):
        return self._max_samples

    @property
    def channel_ranges(self):
        return self._channel_ranges

    @property
    def channel_offsets(self):
        return self._channel_offsets

    @property
    def enabled_sources(self):
        return self._enabled_sources

    @property
    def time_interval(self):
        """The time interval in seconds"""
        return self._time_interval

    @property
    def probe_attenuations(self):
        return self._probe_attenuations

    @probe_attenuations.setter
    def probe_attenuations(self, value):
        self._probe_attenuations = value

    @property
    @requires_open()
    def info(self):
        return self.driver.get_unit_info(self)

    @requires_open("The device either did not initialise correctly or has already been closed.")
    def close(self):
        self.driver.close_unit(self)
        self._handle = None
        self._max_adc = None
        self._buffers.clear()
        self._max_samples = None
        self._channel_ranges.clear()
        self._channel_offsets.clear()
        self._enabled_sources.clear()
        self._time_interval_ns = None
        self._probe_attenuations = DEFAULT_PROBE_ATTENUATION.copy()
        # Reset any cached timebase information if those attributes exist from prior modifications
        if hasattr(self, '_cached_timebase_options'):
            self._cached_timebase_options = None
        if hasattr(self, '_cached_timebase_info'):
            self._cached_timebase_info = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        if all(i is None for i in args):
            return True
        return False

    @requires_open()
    def reset(self):
        """
        Closes and re-opens the connection to the PicoScope.
        Attempts to re-open the same device by serial number if possible.
        Resets internal cached state of this Device object.
        Channel configurations and other settings will need to be reapplied.
        """
        driver = self._driver
        current_serial = None
        resolution_to_use = None

        # Try to get serial number to re-open the same device
        try:
            device_info = driver.get_unit_info(self)
            current_serial = device_info.serial
        except Exception:
            # If serial cannot be fetched, _python_open_unit will open the first available.
            pass

        # Use the driver's default resolution if available for re-opening.
        if hasattr(driver, 'DEFAULT_RESOLUTION'):
            resolution_to_use = driver.DEFAULT_RESOLUTION

        self.close()

        # Re-open the unit
        try:
            new_handle = driver._python_open_unit(serial=current_serial, resolution=resolution_to_use)
            self._handle = new_handle
        except Exception as e:
            self._handle = None
            raise ConnectionError(f"Failed to re-open device during reset: {e}")

        if not self.is_open:
            raise ConnectionError("Device reset failed: handle is invalid after re-open attempt.")

    @requires_open()
    def set_channel(self, channel_name, enabled, coupling='DC', range_peak=float('inf'), analog_offset=0):
        """Configures a single analog channel.

        channel_name: The channel name as a string (e.g., 'A').
        enabled: bool, True to enable the channel, False to disable.
        coupling (optional): 'AC' or 'DC'. Defaults to 'DC'.
        range_peak (optional): Desired +/- peak voltage. The driver selects the best range.
                               Required if enabling the channel.
        analog_offset (optional): The analog offset for the channel in Volts.
        """
        if not enabled:
            self.driver.set_channel(self,
                                    channel_name=channel_name,
                                    enabled=enabled)
            try:
                del self._channel_ranges[channel_name]
                del self._channel_offsets[channel_name]
                self._enabled_sources.remove(channel_name)
            except KeyError:
                pass
            return

        self._channel_ranges[channel_name] = self.driver.set_channel(device=self,
                                                                     channel_name=channel_name,
                                                                     enabled=enabled,
                                                                     coupling=coupling,
                                                                     range_peak=range_peak,
                                                                     analog_offset=analog_offset)
        self._channel_offsets[channel_name] = analog_offset
        self._enabled_sources.add(channel_name)

        return self._channel_ranges[channel_name]

    @requires_open()
    def set_digital_port(self, port_number, enabled, voltage_level=1.8):
        """Set the digital port

        Args:
            port_number (int): identifies the port for digital data. (e.g. 0 for digital channels 0-7)
            enabled (bool): whether or not to enable the channel (boolean)
            voltage_level (float): the voltage at which the state transitions between 0 and 1. Range: –5.0 to 5.0 (V).
        """
        info = self.info
        if not info.variant.decode('utf-8').endswith("MSO"):
            raise FeatureNotSupportedError("This device has no digital ports.")
        self.driver.set_digital_port(device=self, port_number=port_number, enabled=enabled, voltage_level=voltage_level)
        if enabled:
            self._enabled_sources.add(port_number)
        else:
            try:
                self._enabled_sources.remove(port_number)
            except ValueError:
                pass

    @requires_open()
    def set_channels(self, *channel_configs):
        """ set_channels(self, *channel_configs)
        An alternative to calling set_channel for each one, you can call this method with some channel configs.
        This method will also disable any missing channels from the passed configs, and disable ALL channels if the
        collection is empty. """
        # Add channels which are missing as "disabled".
        if len(channel_configs) < len(self.driver.PICO_CHANNEL):
            channel_configs = list(channel_configs)
            present_channels = set(c.name for c in channel_configs)
            missing_channels = [cn for cn in self.driver.PICO_CHANNEL.keys() if cn not in present_channels]
            for channel_name in missing_channels:
                channel_configs.append(ChannelConfig(channel_name, False))

        for channel_config in channel_configs:
            self.set_channel(*channel_config)

    def _timebase_options_are_impossible(self, options):
        device_max_samples_possible = self.driver.MAX_MEMORY
        if options.no_of_samples is not None:
            if options.no_of_samples > device_max_samples_possible:
                return True
        elif options.max_time_interval is not None and options.min_collection_time is not None:
            effective_min_no_samples = math.ceil(options.min_collection_time / options.max_time_interval)
            if effective_min_no_samples > device_max_samples_possible:
                return True
        if None not in (options.no_of_samples, options.max_time_interval, options.min_collection_time):
            # if all 3 are requested, the result can be impossible.
            effective_min_no_samples = int(math.ceil(options.min_collection_time / options.max_time_interval))
            if effective_min_no_samples > options.no_of_samples:
                return True
        # Is it still possible that this device cannot handle this request, but we don't know without making calls to
        # get_timebase.
        return False

    @staticmethod
    def _validate_timebase(timebase_options, timebase_info):
        """validate whether a timebase result matches the options requested."""
        if timebase_options.max_time_interval is not None:
            if timebase_info.time_interval > timebase_options.max_time_interval:
                return False
        if timebase_options.no_of_samples is not None:
            if timebase_options.no_of_samples > timebase_info.max_samples:
                return False
        if timebase_options.min_collection_time is not None:
            if timebase_options.min_collection_time > timebase_info.max_samples * timebase_info.time_interval:
                return False
        return True

    @requires_open()
    def find_timebase(self, timebase_options):
        timebase_id = 0
        # quickly validate that the request is not impossible.
        if self._timebase_options_are_impossible(timebase_options):
            raise NoValidTimebaseForOptionsError()
        # TODO binary search?
        last_error = None
        found_one_good = False
        while True:
            try:
                timebase_info = self.driver.get_timebase(self, timebase_id, 0, timebase_options.oversample)
                found_one_good = True
                if self._validate_timebase(timebase_options, timebase_info):
                    return timebase_info
            except InvalidTimebaseError as e:
                if found_one_good:
                    # we won't find a valid timebase.
                    last_error = e
                    break
            timebase_id += 1
        args = ()
        if last_error is not None:
            args = (last_error.args[0],)
        raise NoValidTimebaseForOptionsError(*args)

    @requires_open()
    def get_timebase(self, timebase_id, no_of_samples, oversample=1, segment_index=0):
        """Query the device about what time precision modes it can handle.

        Returns:
            namedtuple:
                - timebase_id: The id corresponding to the timebase used
                - time_interval: The time interval between readings at the selected timebase.
                - time_units: The unit of time (not supported in e.g. 3000a)
                - max_samples: The maximum number of samples available. The number may vary depending on the number of
                    channels enabled and the timebase chosen.
                - segment_id: The index of the memory segment to use
        """
        timebase_info = self.driver.get_timebase(self, timebase_id, no_of_samples, oversample, segment_index)
        self._time_interval = timebase_info.time_interval
        return timebase_info

    @requires_open()
    def memory_segments(self, number_segments):
        """The number of segments defaults to 1, meaning that each capture fills the scope's available memory.
        This function allows you to divide the memory into a number of segments so that the scope can store several
        waveforms sequentially.

        Returns:
            int: The number of samples available in each segment. This is the total number over all channels,
                so if more than one channel is in use then the number of samples available to each
                channel is max_samples divided by the number of channels.
        """
        return self.driver.memory_segments(self, number_segments)

    @requires_open()
    def maximum_value(self):
        """Get the maximum ADC value for this device."""
        self._max_adc = self.driver.maximum_value(self)
        return self._max_adc

    @requires_open()
    def set_null_trigger(self):
        self.driver.set_null_trigger()

    @requires_open()
    def set_simple_trigger(self, channel, enable=True, threshold_mv=500, direction="FALLING", delay=0,
                           auto_trigger_ms=1000):
        """Set a simple trigger for a channel

        Args:
            channel (str): The channel on which to trigger
            enable (bool): False to disable the trigger, True to enable it
            threshold_mv (int): The threshold in millivolts at which the trigger will fire.
            direction (str): The direction in which the signal must move to cause a trigger.
            delay (int): The time (sample periods) between the trigger occurring and the first sample.
            auto_trigger_ms (int): The number of milliseconds the device will wait if no trigger occurs.
                If this is set to zero, the scope device will wait indefinitely for a trigger.
        """
        if channel not in self.enabled_sources:
            raise ChannelNotEnabledError(f"Channel {channel} is not enabled. Please run set_channel first.")
        if channel not in self.channel_ranges:
            raise InvalidRangeOfChannel(f"The range of channel {channel} is not valid or isn't correctly obtained via"
                                        "set_channel.")
        max_voltage = self.channel_ranges[channel]
        max_adc = self.max_adc if self.max_adc else self.maximum_value()

        self.driver.set_simple_trigger(self, max_voltage, max_adc, enable, channel, threshold_mv, direction, delay,
                                       auto_trigger_ms)

    @requires_open()
    def run_block(self, pre_trigger_samples, post_trigger_samples, timebase_id, oversample=1, segment_index=0):
        """This function starts collecting data in block mode."""
        self._max_samples = pre_trigger_samples + post_trigger_samples
        self.driver.run_block(self, pre_trigger_samples, post_trigger_samples, timebase_id, oversample, segment_index)

    @requires_open()
    def is_ready(self):
        """poll this function to find out when block mode is ready or has triggered.
        returns: True if data is ready, False otherwise."""
        return self.driver.is_ready(self)

    @requires_open()
    def stop_block_capture(self, timeout_minutes=5):
        """Poll the driver to see if it has finished collecting the requested samples.

        Args:
            timeout_minutes (int/float): The timeout in minutes. If the time exceeds the timeout, the poll stops.
        """
        self.driver.stop_block_capture(self, timeout_minutes)

    @requires_open()
    def set_data_buffer(self, channel_or_port, segment_index=0, mode='NONE'):
        """Set the data buffer for a specific channel.

        Args:
            channel_or_port: Channel (e.g. 'A', 'B') or digital port (e.g. 0, 1) to set data for
            buffer_length: The size of the buffer array (equal to no_of_samples)
            segment_index: The number of the memory segment to be used (default is 0)
            mode: The ratio mode to be used (default is 'NONE')
        """
        self._buffers[channel_or_port] = self.driver.set_data_buffer(self, channel_or_port, self.max_samples,
                                                                     segment_index, mode)

    @requires_open()
    def set_all_data_buffers(self, segment_index=0, mode='NONE'):
        """Set the data buffer for each enabled channels and ports

        Args:
            channel_or_port: Channel (e.g. 'A', 'B') or digital port (e.g. 0, 1) to set data for
            buffer_length: The size of the buffer array (equal to no_of_samples)
            segment_index: The number of the memory segment to be used (default is 0)
            mode: The ratio mode to be used (default is 'NONE')
        """
        for channel_or_port in self.enabled_sources:
            self.set_data_buffer(channel_or_port, segment_index, mode)

    @requires_open()
    def get_values(self,start_index=0, downsample_ratio=0,
                   downsample_ratio_mode="NONE", segment_index=0, output_dir=".", filename="data", save_to_file=False,
                   ):
        """Get stored data values from the scope and store it in a clean SingletonScopeDataDict object.

        This function is used after data collection has stopped. It gets the stored data from the scope, with or
        without downsampling, starting at the specified sample number.

        The returned captured data is converted to mV.

        Args:
            start_index (int): A zero-based index that indicates the start point for data collection. It is measured in
                               sample intervals from the start of the buffer.
            downsample_ratio (int): The downsampling factor that will be applied to the raw data.
            downsample_ratio_mode (str): Which downsampling mode to use.
            segment_index (int): Memory segment index
            output_dir (str): The output directory where the json file will be saved.
            filename (str): The name of the json file where the data will be stored
            save_to_file (bool): True if the data has to be saved to a file on the disk, False otherwise
            probe_attenuation (dict): The attenuation factor of the probe used per the channel (1 or 10).

        Returns:
            Tuple of (captured data including time, overflow warnings)
        """
        return self.driver.get_values(self, self.buffers, self.max_samples, self.time_interval, self.channel_ranges,
                                      start_index, downsample_ratio, downsample_ratio_mode, segment_index, output_dir,
                                      filename, save_to_file, self.probe_attenuations)

    @requires_open()
    def set_and_load_data(self, segment_index=0, ratio_mode='NONE', start_index=0, downsample_ratio=0,
                          downsample_ratio_mode="NONE", output_dir=".", filename="data", save_to_file=False):
        """Load values from the device.

        Combines set_data_buffer and get_values to load values from the device.

        Args:
            segment_index (int): Memory segment index
            ratio_mode: The ratio mode to be used (default is 'NONE')
            start_index (int): A zero-based index that indicates the start point for data collection. It is measured in
                sample intervals from the start of the buffer.
            downsample_ratio (int): The downsampling factor that will be applied to the raw data.
            downsample_ratio_mode (str): Which downsampling mode to use.
            output_dir (str): The output directory where the json file will be saved.
            filename (str): The name of the json file where the data will be stored
            save_to_file (bool): True if the data has to be saved to a file on the disk, False otherwise

        Returns:
            Tuple of (captured data including time, overflow warnings)
        """
        self.set_all_data_buffers(segment_index, ratio_mode)

        return self.get_values(start_index, downsample_ratio, downsample_ratio_mode, segment_index, output_dir,
                               filename, save_to_file)

    @requires_open()
    def set_trigger_channel_properties(self, threshold_upper, threshold_upper_hysteresis, threshold_lower,
                                       threshold_lower_hysteresis, channel, threshold_mode, aux_output_enable,
                                       auto_trigger_milliseconds):
        """Set the trigger channel properties for the device.

        Args:
            threshold_upper: Upper threshold in ADC counts
            threshold_upper_hysteresis: Hysteresis for upper threshold in ADC counts
            threshold_lower: Lower threshold in ADC counts
            threshold_lower_hysteresis: Hysteresis for lower threshold in ADC counts
            channel: Channel to set properties for (e.g. 'A', 'B', 'C', 'D')
            threshold_mode: Threshold mode (e.g. "LEVEL", "WINDOW")
            aux_output_enable: Enable auxiliary output (boolean) (Not used in eg. ps2000a, ps3000a, ps4000a)
            auto_trigger_milliseconds: The number of milliseconds for which the scope device will wait for a trigger
                before timing out. If set to zero, the scope device will wait indefinitely for a trigger
        """
        self.driver.set_trigger_channel_properties(self, threshold_upper, threshold_upper_hysteresis, threshold_lower,
                                                   threshold_lower_hysteresis, channel, threshold_mode,
                                                   aux_output_enable, auto_trigger_milliseconds)

    @requires_open()
    def set_digital_channel_trigger(self, channel_number=15, direction="DIRECTION_RISING"):
        """Set a simple trigger on the digital channels.

        Args:
            channel_number (int): The number of the digital channel on which to trigger.(e.g. 0 for D0, 1 for D1,...)
            direction (str): The direction in which the signal must move to cause a trigger.
        """
        self.driver.set_digital_channel_trigger(self, channel_number, direction)

    @requires_open()
    def set_trigger_delay(self, delay):
        """This function sets the post-trigger delay, which causes capture to start a defined time after the
        trigger event.

        For example, if delay=100 then the scope would wait 100 sample periods before sampling.
        At a timebase of 500 MS/s, or 2 ns per sample, the total delay would then be 100 x 2 ns = 200 ns.

        Args:
            delay (int): The time between the trigger occurring and the first sample.
        """
        self.driver.set_trigger_delay(self, delay)

    @requires_open()
    def stop(self):
        """This function stops the scope device from sampling data.
        If this function is called before a trigger event occurs, the oscilloscope may not contain valid data.
        """
        self.driver.stop(self)

    @requires_open()
    def capture_block(self, timebase_options, channel_configs=()):
        """device.capture_block(timebase_options, channel_configs)
        timebase_options: TimebaseOptions object, specifying at least 1 constraint, and optionally oversample.
        channel_configs: a collection of ChannelConfig objects. If present, will be passed to set_channels.
        """
        # set_channel:

        if channel_configs:
            self.set_channels(*channel_configs)

        if len(self._channel_ranges) == 0:
            raise NoChannelsEnabledError("We cannot capture any data if no channels are enabled.")

        # memory_segments:
        USE_SEGMENT_ID=0
        try:
            # always force the number of memory segments on the device to 1 before computing timebases for a one-off
            # block capture.
            max_samples_possible = self.driver.memory_segments(self, USE_SEGMENT_ID+1)
            if timebase_options.no_of_samples is not None and timebase_options.no_of_samples > max_samples_possible.value:
                raise NoValidTimebaseForOptionsError()
        except DeviceCannotSegmentMemoryError:
            pass

        # get_timebase
        timebase_info = self.find_timebase(timebase_options)

        post_trigger_samples = timebase_options.no_of_samples
        pre_trigger_samples = 0

        if post_trigger_samples is None:
            post_trigger_samples = int(math.ceil(timebase_options.min_collection_time / timebase_info.time_interval))

        self.driver.set_null_trigger(self)

        # tell the device to capture something:
        approx_time_busy = self.driver.run_block(self,
                                                 pre_trigger_samples,
                                                 post_trigger_samples,
                                                 timebase_info.timebase_id,
                                                 timebase_options.oversample,
                                                 USE_SEGMENT_ID)

        is_ready = self.driver.is_ready(self)
        while not is_ready:
            time.sleep(approx_time_busy / 5)
            is_ready = self.driver.is_ready(self)

        raw_data, overflow_warnings = self.driver.get_values(self,
                                                             self._channel_ranges.keys(),
                                                             post_trigger_samples,
                                                             USE_SEGMENT_ID)

        self.driver.stop(self)

        times = numpy.linspace(0.,
                               post_trigger_samples * timebase_info.time_interval,
                               post_trigger_samples,
                               dtype=numpy.dtype('float32'))

        voltages = {}

        max_adc = self.max_adc if self.max_adc else self.maximum_value()
        for channel, raw_array in raw_data.items():
            array = raw_array.astype(numpy.dtype('float32'), casting='safe')
            factor = self._channel_ranges[channel] / max_adc
            array = array * factor
            voltages[channel] = array

        return times, voltages, overflow_warnings

    @requires_open()
    def set_sig_gen_built_in(self, offset_voltage=0, pk_to_pk=2000000, wave_type="SINE",
                             start_frequency=10000, stop_frequency=10000, increment=0,
                             dwell_time=1, sweep_type="UP", operation='ES_OFF', shots=0, sweeps=0,
                             trigger_type="RISING", trigger_source="NONE", ext_in_threshold=1):
        """Set up the signal generator to output a built-in waveform.

        Args:
            offset_voltage: Offset voltage in microvolts (default 0)
            pk_to_pk: Peak-to-peak voltage in microvolts (default 2000000)
            wave_type: Type of waveform (e.g. "SINE", "SQUARE", "TRIANGLE")
            start_frequency: Start frequency in Hz (default 1000.0)
            stop_frequency: Stop frequency in Hz (default 1000.0)
            increment: Frequency increment in Hz (default 0.0)
            dwell_time: Time at each frequency in seconds (default 1.0)
            sweep_type: Sweep type (e.g. "UP", "DOWN", "UPDOWN")
            operation: Configures the white noise/PRBS (e.g. "ES_OFF", "WHITENOISE", "PRBS")
            shots: Number of shots per trigger (default 1)
            sweeps: Number of sweeps (default 1)
            trigger_type: Type of trigger (e.g. "RISING", "FALLING")
            trigger_source: Source of trigger (e.g. "NONE", "SCOPE_TRIG")
            ext_in_threshold: External trigger threshold in ADC counts
        """
        self.driver.set_sig_gen_built_in(self, offset_voltage, pk_to_pk, wave_type, start_frequency, stop_frequency,
                                         increment, dwell_time, sweep_type, operation, shots, sweeps, trigger_type,
                                         trigger_source, ext_in_threshold)
