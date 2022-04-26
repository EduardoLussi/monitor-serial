class DeviceType:
    def __init__(self):
        self.name = ''
        self.img = ''
        self.byteId = ''
        self.attributes = []

    def getLengthAttributes(self):
        size = 0
        for attr in self.attributes:
            size += attr.size
        return size
