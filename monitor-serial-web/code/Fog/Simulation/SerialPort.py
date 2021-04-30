from datetime import datetime

from time import sleep

from random import randint

from Beans.Device import Device
from Beans.Payload import Payload
from Beans.PayloadAttribute import PayloadAttribute

from DAOs.PayloadAttributeDAO import PayloadAttributeDAO
from DAOs.DeviceDAO import DeviceDAO


class SerialPort:
    def __init__(self):
        self.id = 0
        self.portName = ''
        self.baudRate = 115200
        self._connection = ''
        self.device = Device()
        self.isConnected = False
        self.isReading = False
        self.readingRate = 0

        self.maxReadingRate = 1000

        self.__intervalA = 0
        self.observers = {}

    @staticmethod
    def getPorts():
        result = []

        result.append('COM1')
        result.append('COM2')
        result.append('COM4')

        return result

    def setDevice(self):
        self.connect()

        if self.portName == 'COM1':
            read = '11'
        elif self.portName == 'COM2':
            read = '12'
        else:
            read = '14'

        deviceDao = DeviceDAO()
        device = deviceDao.getDevice(read)
        print(device.id, device.name, device.byteId)
        device.address = "AAA8"

        self.disconnect()

        self.device = device
        self.id = self.device.id

        return True

    def connect(self):
        self.isConnected = True
        return self.isConnected

    def disconnect(self):
        self.isConnected = False
        self.isReading = False
        paDao = PayloadAttributeDAO()
        self.observers['sio'].start_background_task(paDao.commitDB)
        self.observers['deviceStatus'](self.id)

    def send(self, message):
        return True

    def read(self):
        if self.isConnected:
            while len(self.device.payload) <= 0:
                continue
            return self.device.payload[-1].toDict()
        else:
            return False

    def monitor(self):
        self.connect()

        paDao = PayloadAttributeDAO()

        flagFirstExec = True
        contDb = 0
        now = 0
        contPackets = 0
        self.isReading = True
        self.observers['deviceStatus'](self.id)
        while self.isConnected:
            self.connect()

            payload = Payload()
            payload.date = datetime.now()

            byteId = ''
            length = self.device.getLengthAttributes()

            for i, attribute in enumerate(self.device.attributes):
                value = ''
                for j in range(attribute.size):
                    value += str(randint(0, 9))

                payloadAttribute = PayloadAttribute()
                payloadAttribute.attribute = attribute
                payloadAttribute.value = value

                payload.payloadAttributes.append(payloadAttribute)

            try:
                self.observers['sio'].start_background_task(paDao.insertPayload, self.device, payload)
            except Exception as err:
                print(err)

            self.device.payload.clear()
            self.device.payload.append(payload)
            self.observers['devicePayload'](self.id, payload)

            if flagFirstExec:
                contPackets = 0
                now = datetime.now()
            elif (datetime.now() - now).seconds > 1:
                self.readingRate = contPackets

                contPackets = 0
                now = datetime.now()

                contDb += 1
                if contDb == 5:
                    self.observers['sio'].start_background_task(paDao.commitDB)
                    contDb = 0

                self.observers['deviceStatus'](self.id)

                if int(self.readingRate) > int(self.maxReadingRate):
                    print("Packet rate is over the limit")
                    self.disconnect()
                    return

            flagFirstExec = False
            contPackets += 1

            sleep(0.5)
