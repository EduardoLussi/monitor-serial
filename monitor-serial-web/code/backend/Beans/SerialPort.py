from sys import platform
from datetime import datetime

import glob
import serial
from concurrent.futures import ThreadPoolExecutor
import threading

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

        self.maxReadingRate = 1500

        self.__intervalA = 0
        self.__lock = threading.Lock()
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
            read = self._connection.read(1).hex()
            address = self._connection.read(2).hex()
        except Exception as err:
            print(err)
            self.disconnect()
            return False

        deviceDao = DeviceDAO()
        device = deviceDao.getDevice(read)

        device.address = str(address)

        length = device.getLengthAttributes()
        for i in range(length + 1):
            try:
                byteId = self._connection.read(1).hex()
            except Exception as err:
                print(err)
                return False

            if byteId == device.byteId:
                if i == length:
                    break
                print("Package is incorrect")
                return False

        if device is False:
            self.disconnect()
            return False

        self.disconnect()

        if device.attributes is False:
            return False

        self.device = device

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
            self._connection.close()
            self.isConnected = False
            self.isReading = False
            paDao = PayloadAttributeDAO()
            thCommit = threading.Thread(target=paDao.commitDB, args=(self.__lock, ''))
            thCommit.start()
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

    def monitor(self):
        self.connect()

        paDao = PayloadAttributeDAO()

        flagFirstExec = True
        now = 0
        contPackets = 0
        self.isReading = True
        self.observers['deviceStatus'](self.id)
        while self.isConnected:
            if not self.connect():
                self.disconnect()
                return

            payload = Payload()
            payload.date = datetime.now()

            byteId = ''
            length = self.device.getLengthAttributes()
            for i in range(length):
                try:
                    byteId = self._connection.read(1).hex()
                except Exception as err:
                    print(err)
                    self.disconnect()
                    return

                if byteId == self.device.byteId:
                    break

                if i == length - 1:
                    print("Id not recognized")
                    self.disconnect()
                    return

            try:
                address = self._connection.read(2).hex()
            except Exception as err:
                print(err)
                self.disconnect()
                return

            if address != self.device.address:
                print("Address not recognized")
                self.disconnect()
                break

            for i, attribute in enumerate(self.device.attributes):
                value = ''
                for j in range(attribute.size):
                    try:
                        read = chr(int(str(self._connection.read(1).hex().upper()), 16))
                    except Exception as err:
                        print(err)
                        self.disconnect()
                        return
                    value += str(read)

                payloadAttribute = PayloadAttribute()
                payloadAttribute.attribute = attribute
                payloadAttribute.value = value

                payload.payloadAttributes.append(payloadAttribute)

            try:
                th = threading.Thread(target=paDao.insertPayload, args=(self.device, payload, self.__lock))
                th.start()
            except Exception as err:
                print(err)

            self.device.payload.clear()
            self.device.payload.append(payload)
            self.observers['devicePayload'](self.id, payload)

            if flagFirstExec:
                contPackets = 0
                now = datetime.now()
            elif (datetime.now() - now).seconds > 5:
                self.readingRate = round(contPackets / 5)

                contPackets = 0
                now = datetime.now()

                thCommit = threading.Thread(target=paDao.commitDB, args=(self.__lock, ''))
                thCommit.start()

                if int(self.readingRate) > int(self.maxReadingRate):
                    print("Packet rate is over the limit")
                    self.disconnect()
                    return

            flagFirstExec = False
            contPackets += 1
