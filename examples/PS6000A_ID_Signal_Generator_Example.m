%% PicoScope 6000 Series (A API) Instrument Driver Oscilloscope Signal Generator Example
% This is an example of an instrument control session using a device 
% object. The instrument control session comprises all the steps you 
% are likely to take when communicating with your instrument. 
%       
% These steps are:
%    
% # Create a device object   
% # Connect to the instrument 
% # Configure properties 
% # Invoke functions 
% # Disconnect from the instrument 
%
% To run the instrument control session, type the name of the file,
% PS6000A_ID_Signal_Generator_Example, at the MATLAB command prompt.
% 
% The file, PS6000A_ID_SIGNAL_GENERATOR_EXAMPLE.M must be on your MATLAB PATH. For
% additional information on setting your MATLAB PATH, type 'help addpath'
% at the MATLAB command prompt.
%
% *Example:*
%     PS6000A_ID_Signal_Generator_Example;
%
% *Description:*
%     Demonstrates how to set properties and call functions in order to
%     output from the signal generator of a PicoScope 6000 (A API) Series Oscilloscope.
%
% *See also:* <matlab:doc('icdevice') |icdevice|> | <matlab:doc('instrument/invoke') |invoke|>
%
% *Copyright:* © 2020-2022 Pico Technology Ltd. See LICENSE file for terms.

%% Clear Command Window and Close Figures

clc;
close all;

%% Load Configuration Information

[ps6000aStructs, ps6000aEnumInfo]=PS6000aSetConfig();

%% Device Connection

% Check if an Instrument session using the device object 'ps6000DeviceObj'
% is still open, and if so, disconnect if the User chooses 'Yes' when prompted.
if (exist('ps6000aDeviceObj', 'var') && ps6000aDeviceObj.isvalid && strcmp(ps6000aDeviceObj.status, 'open'))
    
    openDevice = questionDialog(['Device object ps6000aDeviceObj has an open connection. ' ...
        'Do you wish to close the connection and continue?'], ...
        'Device Object Connection Open');
    
    if (openDevice == PicoConstants.TRUE)
        
        % Close connection to device
        disconnect(ps6000aDeviceObj);
        delete(ps6000aDeviceObj);
        
    else

        % Exit script if User selects 'No'
        return;
        
    end
    
end

%% Create a device object. 
% The serial number can be specified as a second input parameter.

ps6000aDeviceObj = icdevice('picotech_ps6000a_generic.mdd','');

%% Connect scope

connect(ps6000aDeviceObj)

%% Setup scope to output 2 Vpp 10 kHz Sine wave

% set waveform type to sine wave
waveType = ps6000aEnumInfo.enPicoWaveType.PICO_SINE;

[status.sigGenWaveform] = invoke(ps6000aDeviceObj,'ps6000aSigGenWaveform',waveType, 0,0);

% set output voltage to 2 V peak to peak with 0 V offset

[status.sigGenRange] = invoke(ps6000aDeviceObj, 'ps6000aSigGenRange', 2,0);

% set output frequency
frequency = 10000; %Hz

[status.sigGenFrequency] = invoke(ps6000aDeviceObj, 'ps6000aSigGenFrequency',frequency);

% apply sign generator settings and start generation

sigGenEnabled = 1;
sweepEnabled = 0;
triggerEnabled = 0;
automaticClockOptimisationEnabled = 0;
overrideAutomaticClockAndPrescale = 0;
pFrequency = libpointer('doublePtr',frequency);
stopFrequency = frequency;
pStopFrequency = libpointer('doublePtr',stopFrequency);
frequencyIncrement = 1;
pFrequencyIncrement = libpointer('doublePtr',frequencyIncrement);
dwellTime = 1;
pDwellTime = libpointer('doublePtr',dwellTime);

[status.sigGenApply] = invoke(ps6000aDeviceObj, 'ps6000aSigGenApply', sigGenEnabled, sweepEnabled, triggerEnabled, automaticClockOptimisationEnabled, overrideAutomaticClockAndPrescale, pFrequency, pStopFrequency, pFrequencyIncrement, pDwellTime);

pause(5)

%% change frequency to 100 kHz

frequency = 100000; %Hz
pFrequency = libpointer('doublePtr',frequency);

[status.sigGenFrequency] = invoke(ps6000aDeviceObj, 'ps6000aSigGenFrequency',frequency);

% apply changes
[status.sigGenApply] = invoke(ps6000aDeviceObj, 'ps6000aSigGenApply', sigGenEnabled, sweepEnabled, triggerEnabled, automaticClockOptimisationEnabled, overrideAutomaticClockAndPrescale, pFrequency, pStopFrequency, pFrequencyIncrement, pDwellTime);

pause(5)

%% sweep frequency from 100 kHz to 1 mHz over ~1 s

stopFrequency = 1000000;
frequencyIncrement = 10000;
dwellTime = 0.01;
sweepType = ps6000aEnumInfo.enPicoSweepType.PICO_UPDOWN;

[status.sigGenFrequencySweep] = invoke(ps6000aDeviceObj,'ps6000aSigGenFrequencySweep',stopFrequency,frequencyIncrement,dwellTime,sweepType);

% apply changes
sweepEnabled = 1;
pStopFrequency = libpointer('doublePtr',stopFrequency);
pFrequencyIncrement = libpointer('doublePtr',frequencyIncrement);
pDwellTime = libpointer('doublePtr',dwellTime);
[status.sigGenApply] = invoke(ps6000aDeviceObj, 'ps6000aSigGenApply', sigGenEnabled, sweepEnabled, triggerEnabled, automaticClockOptimisationEnabled, overrideAutomaticClockAndPrescale, pFrequency, pStopFrequency, pFrequencyIncrement, pDwellTime);

pause(5)

%% change wave type to square and stop sweeping

waveType = ps6000aEnumInfo.enPicoWaveType.PICO_SQUARE;

[status.sigGenWaveform] = invoke(ps6000aDeviceObj,'ps6000aSigGenWaveform',waveType, 0,0);

% apply changes
sweepEnabled = 0;
[status.sigGenApply] = invoke(ps6000aDeviceObj, 'ps6000aSigGenApply', sigGenEnabled, sweepEnabled, triggerEnabled, automaticClockOptimisationEnabled, overrideAutomaticClockAndPrescale, pFrequency, pStopFrequency, pFrequencyIncrement, pDwellTime);

pause(5)

%% Disconnect scope

disconnect(ps6000aDeviceObj);

%%
delete(ps6000aDeviceObj);
