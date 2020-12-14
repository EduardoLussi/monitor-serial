from DAOs.PayloadAttributeDAO import PayloadAttributeDAO


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

    def getReading(self, fromDate, toDate, attribute):
        paDao = PayloadAttributeDAO()
        values = paDao.getValues(self, attribute, fromDate, toDate)

        if values is False:
            return False

        valuesList = []
        datesList = []
        for value in values:
            datesList.append(value[1])
            valuesList.append(int(value[0]))

        return {
            'values': valuesList,
            'dates': datesList
        }

