from sys import platform
from datetime import datetime
from threading import Thread
from time import sleep

import glob
import serial

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
        self.paDao = PayloadAttributeDAO()
        self.__intervalA = 0
        self.observers = {}

    @staticmethod
    def getPorts():
        if platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif platform.startswith('linux') or platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        return result

    def setDevice(self):
        if not self.connect():
            return False

        try:
            read = self._connection.readline()[:-2]
        except Exception as err:
            print(err)
            self.disconnect()
            return False

        deviceDao = DeviceDAO()
        byteId = str(hex(read[0]))[2:]
        device = deviceDao.getDevice(byteId)
        address = str(hex(read[1]))[2:]
        address += str(hex(read[2]))[2:]
        device.address = str(address)

        if device is False or device.attributes is False or len(read) != device.getLengthAttributes() + 3:
            self.disconnect()
            return False

        self.disconnect()

        self.device = device
        self.id = self.device.id

        return True

    def connect(self):
        if self.isConnected:
            return True

        try:
            self._connection = serial.Serial(self.portName, self.baudRate)
        except Exception as err:
            print(err)
            return False

        self.isConnected = True

        return True

    def disconnect(self):
        try:
            self.paDao.queueFlag = False
            self._connection.close()
            self.isConnected = False
            self.isReading = False
            paDao = PayloadAttributeDAO()

            self.observers['sio'].start_background_task(paDao.commitDB)
            self.observers['deviceStatus'](self.id)
        except Exception as err:
            print(err)

    def send(self, message):
        if self.isConnected:
            try:
                self._connection.write(bytes(message, 'utf-8'))
            except Exception as err:
                print(err)
                return False
            return True
        return False

    def read(self):
        if self.isConnected:
            while len(self.device.payload) <= 0:
                continue
            return self.device.payload[-1].toDict()
        else:
            return False

    def monitor2(self):
        self.connect()

        pcks = 0
        now = datetime.today()
        readings = []
        while self.isConnected:
            # read = ''
            # for i in range(10):
            #     read += conn.read(1).hex()
            read = str(self._connection.readline()).replace(r"\r\n'", '').replace("b'", '')
            read = read[1:]
            pcks += 1
            # print(read)
            readings.append(read)
            if (datetime.today() - now).seconds >= 1:
                print(pcks)
                now = datetime.today()
                readings.clear()
                pcks = 0
        return

    def monitor(self):
        self.paDao.queueFlag = True
        self.connect()
        self._connection.readline()
        self.observers['sio'].start_background_task(self.paDao.payloadQueueConsumer)
        contPackets = 0
        self.isReading = True
        self.observers['deviceStatus'](self.id)
        now = datetime.now()
        while self.isConnected:
            if not self.connect():
                self.disconnect()
                return

            contPackets += 1
            payload = Payload()
            payload.date = datetime.now()
            try:
                read = self._connection.readline()[:-2]
            except Exception as err:
                print(err)
                self.disconnect()
                return

            byteId = str(hex(read[0]))[2:]
            address = str(hex(read[1]))[2:]
            address += str(hex(read[2]))[2:]

            if byteId != self.device.byteId or len(read) != self.device.getLengthAttributes() + 3:
                self.disconnect()
                print("Packet not recognized")
                return

            i = 3
            for attribute in self.device.attributes:
                value = ''
                for _ in range(attribute.size):
                    value += chr(int(hex(read[i]), 16))
                    i += 1

                payloadAttribute = PayloadAttribute()
                payloadAttribute.attribute = attribute
                payloadAttribute.value = value

                payload.payloadAttributes.append(payloadAttribute)

            # Insere payload na fila de inserção
            self.paDao.queue.put((self.device, payload))

            self.device.payload.clear()
            self.device.payload.append(payload)

            if (datetime.now() - now).seconds >= 1:
                self.observers['devicePayload'](self.id, payload)
                self.readingRate = contPackets

                contPackets = 0

                self.observers['deviceStatus'](self.id)

                if int(self.readingRate) > int(self.maxReadingRate):
                    print("Packet rate is over the limit")
                    self.disconnect()
                    return

                now = datetime.now()
