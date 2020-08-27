from sys import platform
import glob
import serial
from threading import Lock
import datetime

class SerialPort:
    def __init__(self):
        self.isReading = False
        self.port = 'COM3'
        self.baudrate = 115200
        self.showTime = True
        self._connection = ''

    @staticmethod
    def serial_ports():
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

    def connect(self):
        try:
            self._connection = serial.Serial(self.port, self.baudrate)
        except Exception as err:
            print(err)
            return 'false'
        self.isReading = True
        return 'true'

    def disconnect(self):
        if self._connection != '':
            self._connection.close()
        self.isReading = False

    def serial_write(self, command):
        try:
            self._connection.write(bytes(command, "utf-8"))
        except Exception as err:
            print(err)
            return 'false'
        return 'true'

    def serial_read(self):
        bytesToRead = int(self._connection.inWaiting())
        while bytesToRead == 0:
            bytesToRead = int(self._connection.inWaiting())

        read = self._connection.read(bytesToRead)

        try:
            read = read.decode('utf-8').rstrip('\n')
        except Exception as err:
            print(err)

        insert = ''
        if self.showTime:
            insert += (str(datetime.datetime.today())[:19]) + ' -> ' + read
        else:
            insert += read

        return insert

