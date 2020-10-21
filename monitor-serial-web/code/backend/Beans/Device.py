class Device:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.img = ''
        self.byteId = b'\00'
        self.attributes = []
        self.payload = []
        self.address = ''

    def getLengthAttributes(self):
        size = 0
        for attr in self.attributes:
            size += attr.size
        return size
