%% PicoScope 6000 Series (A API) Instrument Driver Oscilloscope Block Data Capture Example
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
% PS6000A_ID_Block_Example, at the MATLAB command prompt.
% 
% The file, PS6000A_ID_BLOCK_EXAMPLE.M must be on your MATLAB PATH. For
% additional information on setting your MATLAB PATH, type 'help addpath'
% at the MATLAB command prompt.
%
% *Example:*
%     PS6000A_ID_Block_Example;
%
% *Description:*
%     Demonstrates how to set properties and call functions in order to
%     capture a block of data from a PicoScope 6000 (A API) Series Oscilloscope.
%
% *See also:* <matlab:doc('icdevice') |icdevice|> | <matlab:doc('instrument/invoke') |invoke|>
%
% *Copyright:* © 2020 Pico Technology Ltd. See LICENSE file for terms.

%% Suggested Input Settings

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

%% Set Device Resolution

resolution = ps6000aEnumInfo.enPicoDeviceResolution.PICO_DR_10BIT;

[status.setResolution] = invoke(ps6000aDeviceObj, 'ps6000aSetDeviceResolution', resolution);

disp('Device Resolution set to 10 bits')

%% Enable Channel A + B
% Enable channels A + B with +-5 V range with DC coupling and full bandwidth

channelA = ps6000aEnumInfo.enPicoChannel.PICO_CHANNEL_A;
channelB = ps6000aEnumInfo.enPicoChannel.PICO_CHANNEL_B;
couplingDC = ps6000aEnumInfo.enPicoCoupling.PICO_DC;
range = ps6000aEnumInfo.enPicoConnectProbeRange.PICO_X1_PROBE_5V;
bandwidth = ps6000aEnumInfo.enPicoBandwidthLimiter.PICO_BW_FULL;


[status.setChannelOn.A] = invoke(ps6000aDeviceObj, 'ps6000aSetChannelOn', channelA, couplingDC, range, 0, bandwidth);
[status.setChannelOn.B] = invoke(ps6000aDeviceObj, 'ps6000aSetChannelOn', channelB, couplingDC, range, 0, bandwidth);

disp('Channels A and B set')

% Disable all other channels
for i = (2:7)
    try
        [status.setChannelOff] = invoke(ps6000aDeviceObj, 'ps6000aSetChannelOff', i);
    catch
        
    end 
end

disp('Remaining Channels disabled')

%% Set Simple Trigger

enable = 1;
source = channelA;
threshold = 1000; %mV
direction = ps6000aEnumInfo.enPicoThresholdDirection.PICO_RISING;
delay = 0;
autoTriggerMicroSeconds = 1000000; %us

[status.setSimpleTrigger] = invoke(ps6000aDeviceObj, 'ps6000aSetSimpleTrigger', enable, source, threshold, direction,...
    delay, autoTriggerMicroSeconds);

disp('Simple Trigger set')


%% Get Fastest Timebase

enabledChannelFlags= ps6000aEnumInfo.enPicoChannelFlags.PICO_CHANNEL_A_FLAGS + ps6000aEnumInfo.enPicoChannelFlags.PICO_CHANNEL_B_FLAGS;
pTimebase = libpointer('uint32Ptr',0);
pTimeInterval = libpointer('doublePtr',0);

[status.getMinimumTimebaseStateless] = invoke(ps6000aDeviceObj, 'ps6000aGetMinimumTimebaseStateless', enabledChannelFlags,...
    pTimebase, pTimeInterval, resolution);

timebase = pTimebase.Value;
timeInterval = pTimeInterval.Value;

%% Set number of samples to be collected

numPreTriggerSamples = 1000000;
numPostTriggerSamples = 9000000;
totalSamples = numPreTriggerSamples + numPostTriggerSamples;

%% Create Buffers

bufferAMax = zeros(totalSamples, 1, 'int16');
bufferBMax = zeros(totalSamples, 1, 'int16');
bufferAMin = zeros(totalSamples, 1, 'int16');
bufferBMin = zeros(totalSamples, 1, 'int16');
pBufferAMax =libpointer('int16Ptr', bufferAMax);
pBufferBMax =libpointer('int16Ptr', bufferBMax);
pBufferAMin =libpointer('int16Ptr', bufferAMin);
pBufferBMin =libpointer('int16Ptr', bufferBMin);

dataType = ps6000aEnumInfo.enPicoDataType.PICO_INT16_T;
waveform = 0;
downSampleRatioMode = ps6000aEnumInfo.enPicoRatioMode.PICO_RATIO_MODE_AVERAGE;
actionA = bitor(ps6000aEnumInfo.enPicoAction.PICO_CLEAR_ALL, ps6000aEnumInfo.enPicoAction.PICO_ADD);
actionB = ps6000aEnumInfo.enPicoAction.PICO_ADD;

[status.setBufferA] = invoke(ps6000aDeviceObj, 'ps6000aSetDataBuffers', channelA, pBufferAMax, ...
    pBufferAMin, totalSamples, dataType, waveform, downSampleRatioMode, actionA);
[status.setBufferB] = invoke(ps6000aDeviceObj, 'ps6000aSetDataBuffers', channelB, pBufferBMax, ...
    pBufferBMin, totalSamples, dataType, waveform, downSampleRatioMode, actionB);

%% Run Block Capture

pTimeIndisposedMs = libpointer('doublePtr',0);
segmentIndex = 0;

disp('Collection starting...')

[status.runBlock] = invoke(ps6000aDeviceObj, 'ps6000aRunBlock', numPreTriggerSamples, numPostTriggerSamples,...
    timebase, pTimeIndisposedMs, segmentIndex); 

pReady = libpointer('int16Ptr',0);

while pReady.Value == 0
    [status.IsReady] = invoke(ps6000aDeviceObj,'ps6000aIsReady',pReady);
end

disp('Collection finished')

%% Retrieve Data

startIndex = 0;
pSamplesCollected = libpointer('uint64Ptr',totalSamples);
downSampleRatio = 1;
segmentIndex = 0;
pOverflow = libpointer('int16Ptr',0);

[status.getValues] = invoke(ps6000aDeviceObj,'ps6000aGetValues', startIndex,...
    pSamplesCollected, downSampleRatio, downSampleRatioMode, segmentIndex, pOverflow);

samplesCollected = pSamplesCollected.Value;

disp('Data Retrieved')

%% Convert Data from ADC counts to mV

bufferAMax = pBufferAMax.Value;
bufferAMin = pBufferAMin.Value;
bufferBMax = pBufferBMax.Value;
bufferBMin = pBufferBMin.Value;

pMinValue = libpointer('int16Ptr',0);
pMaxValue = libpointer('int16Ptr',0);

[status.getAdcLimits] = invoke(ps6000aDeviceObj, 'ps6000aGetAdcLimits', resolution, pMinValue, pMaxValue);

minValue = pMinValue.Value;
maxValue = pMaxValue.Value;

voltageRange = 5000; %mV

bufferAMax = adc2mv(bufferAMax,voltageRange,double(maxValue));
bufferBMax = adc2mv(bufferBMax,voltageRange,double(maxValue));

disp('Data converted to mV')

%% Plot Collected Data

maxTime = (double(samplesCollected) * timeInterval);
time = linspace(0,maxTime,samplesCollected);

figure(1)
plot(time,bufferAMax);
hold on
plot(time,bufferBMax);
ylabel('Voltage (mV)');
xlabel('Time (s)');
hold off

%% Disconnect scope

disconnect(ps6000aDeviceObj);

%%

delete(ps6000aDeviceObj);