from picosdk.ps2000 import ps2000

with ps2000.open_unit() as device:
    print('Device info: {}'.format(device.info))
