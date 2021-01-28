%% PicoScope 6000 Series (A API) Instrument Driver Oscilloscope Streaming Data Capture Example
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
% PS6000A_ID_Streaming_Example, at the MATLAB command prompt.
% 
% The file, PS6000A_ID_STREAMING_EXAMPLE.M must be on your MATLAB PATH. For
% additional information on setting your MATLAB PATH, type 'help addpath'
% at the MATLAB command prompt.
%
% *Example:*
%     PS6000A_ID_Streaming_Example;
%
% *Description:*
%     Demonstrates how to set properties and call functions in order to
%     stream data from a PicoScope 6000 (A API) Series Oscilloscope.
%
% *See also:* <matlab:doc('icdevice') |icdevice|> | <matlab:doc('instrument/invoke') |invoke|>
%
% *Copyright:* © 2021 Pico Technology Ltd. See LICENSE file for terms.

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
% Disable  other channels
for i = (0:7)
    try
        [status.setChannelOff] = invoke(ps6000aDeviceObj, 'ps6000aSetChannelOff', i);
    catch
        
    end 
end

for j = (128:1:131)
    try
        [status.turnDigitalPortOff] = invoke(ps6000aDeviceObj, 'ps6000aDigitalPortOff',j);
    catch
    end
end

% Enable channels A + B with +-5 V range with DC coupling and full bandwidth

channelA = ps6000aEnumInfo.enPicoChannel.PICO_CHANNEL_A;
couplingDC = ps6000aEnumInfo.enPicoCoupling.PICO_DC;
range = ps6000aEnumInfo.enPicoConnectProbeRange.PICO_X1_PROBE_5V;
bandwidth = ps6000aEnumInfo.enPicoBandwidthLimiter.PICO_BW_FULL;


[status.setChannelOn.A] = invoke(ps6000aDeviceObj, 'ps6000aSetChannelOn', channelA, couplingDC, range, 0, bandwidth);

disp('Channels A set')

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

%% Set number of samples to be collected

numPreTriggerSamples = 100000;
numPostTriggerSamples = 900000;
totalSamples = numPreTriggerSamples + numPostTriggerSamples;

%% Create Buffers

bufferA = zeros(totalSamples, 1, 'int16');

maxBuffers = 10;

for i =(1:maxBuffers)
    pBufferA(i,1) =libpointer('int16Ptr', bufferA);
end


dataType = ps6000aEnumInfo.enPicoDataType.PICO_INT16_T;
waveform = 0;
downSampleRatioMode = ps6000aEnumInfo.enPicoRatioMode.PICO_RATIO_MODE_AVERAGE;
actionA = bitor(ps6000aEnumInfo.enPicoAction.PICO_CLEAR_ALL, ps6000aEnumInfo.enPicoAction.PICO_ADD);
actionB = ps6000aEnumInfo.enPicoAction.PICO_ADD;


[status.setBufferA] = invoke(ps6000aDeviceObj, 'ps6000aSetDataBuffer', channelA, pBufferA(1,1), ...
    totalSamples, dataType, waveform, downSampleRatioMode, actionA);


%% Run Block Capture

sampleInterval = 1;
sampleIntervalTimeUnits = ps6000aEnumInfo.enPicoTimeUnits.PICO_US;
autoStop = 1;
downSampleRatio = 1;

disp('Streaming starting...')

[status.runStreaming] = invoke(ps6000aDeviceObj, 'ps6000aRunStreaming', sampleInterval, sampleIntervalTimeUnits,...
    numPreTriggerSamples, numPostTriggerSamples, autoStop, downSampleRatio, downSampleRatioMode);
%%

streamData = ps6000aStructs.tPicoStreamingDataInfo.members;

streamData.bufferIndex_ = 0;
streamData.channel_ = ps6000aEnumInfo.enPicoChannel.PICO_CHANNEL_A;
streamData.mode_ = ps6000aEnumInfo.enPicoRatioMode.PICO_RATIO_MODE_AVERAGE;
streamData.noOfSamples_ = 0;
streamData.overflow_ = 0;
streamData.startIndex_ = 0;
streamData.type_ = ps6000aEnumInfo.enPicoDataType.PICO_INT16_T;

pStreamData = libpointer('tPicoStreamingDataInfoPtr',streamData);

streamTrigger = ps6000aStructs.tPicoStreamingDataTriggerInfo.members;
streamTrigger.triggerAt_=0;
streamTrigger.triggered_=0;
streamTrigger.autoStop_=0;

pStreamTrigger = libpointer('tPicoStreamingDataTriggerInfoPtr',streamTrigger);
%%
i=1
while i < maxBuffers
    
    pause(0.25)

    [status.getStreamingLatestValues] = invoke(ps6000aDeviceObj, 'ps6000aGetStreamingLatestValues', pStreamData, 1, pStreamTrigger);
    
    if status.getStreamingLatestValues ~= 0
        bufferA(:,i) = pBufferA(i,1).Value;
        i=i+1
        [status.setBufferA] = invoke(ps6000aDeviceObj, 'ps6000aSetDataBuffer', channelA, pBufferA(i,1), ...
    totalSamples, dataType, waveform, downSampleRatioMode, actionB);
    end
        
end

disp('Streaming finished')

%% Convert Data from ADC counts to mV

pMinValue = libpointer('int16Ptr',0);
pMaxValue = libpointer('int16Ptr',0);

[status.getAdcLimits] = invoke(ps6000aDeviceObj, 'ps6000aGetAdcLimits', resolution, pMinValue, pMaxValue);

minValue = pMinValue.Value;
maxValue = pMaxValue.Value;

voltageRange = 5000; %mV

bufferA = pBufferA.Value;

bufferA = adc2mv(bufferA,voltageRange,double(maxValue));

disp('Data converted to mV')

%% Plot Collected Data

samplesCollected=length(bufferA(:,1));
maxTime = (double(samplesCollected) * sampleInterval);
timeUS = linspace(0,maxTime,samplesCollected);

figure(1)
plot(timeUS,bufferA(:,1));
hold on
ylabel('Voltage (mV)');
xlabel('Time (us)');
hold off

%% Disconnect scope

disconnect(ps6000aDeviceObj);

%%

delete(ps6000aDeviceObj);