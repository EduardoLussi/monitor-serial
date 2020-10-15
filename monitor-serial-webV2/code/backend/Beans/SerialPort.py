from sys import platform
from datetime import datetime
import glob
import serial

from Beans.Device import Device
from Beans.Payload import Payload
from Beans.PayloadAttribute import PayloadAttribute

from DAOs.DeviceDAO import DeviceDAO


class SerialPort:
    def __init__(self):
        self.id = 0
        self.portName = ''
        self.baudRate = 115200
        self._connection = ''
        self.device = Device()
        self.isConnected = False

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
        if len(result) == 0:
            return False

        return result

    def setDevice(self):
        if not self.connect():
            return False

        try:
            read = self._connection.read(1).hex()
        except Exception as err:
            print(err)
            self.disconnect()
            return False

        self.disconnect()

        deviceDao = DeviceDAO()
        device = deviceDao.getDevice(read)

        if device is False:
            return False

        device.attributes = deviceDao.getAttributes(device)
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
        except Exception as err:
            print(err)

    def send(self):
        pass

    def read(self):
        if not self.connect():
            return False

        payload = Payload()
        payload.date = datetime.now()

        read = self._connection.read(1)

        for i, attribute in enumerate(self.device.attributes):

            value = ''
            for j in range(attribute.size):
                try:
                    read = chr(int(str(self._connection.read(1).hex().upper()), 16))
                except Exception as err:
                    print(err)
                    self.disconnect()
                    return False
                value += str(read)

            payloadAttribute = PayloadAttribute()
            payloadAttribute.attribute = attribute
            payloadAttribute.value = value

            payload.payloadAttributes.append(payloadAttribute)

        self.device.payload.append(payload)

        return payload.toDict()
