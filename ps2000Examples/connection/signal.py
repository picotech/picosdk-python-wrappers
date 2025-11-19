class Data:
    def __init__(self, object=None):
        self.type = type(object).__name__
        if object is None:
            self.data = []
        else:
            self.data = object


class Settings:
    def __init__(self, voltage=5.0, frequency=50.0, time=1.0, pulses=10):
        self.voltage = voltage
        self.frequency = frequency
        self.time = time
        self.pulses = pulses
    

