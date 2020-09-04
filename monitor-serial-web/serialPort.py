from sys import platform
import glob
import serial
from threading import Lock
import datetime
from pdu import *


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

        attributes = []
        values = []

        pdu = PDU_DEFAULT['attribute']
        size = PDU_DEFAULT['size']
        payload = PDU_DEFAULT['payload']

        address = ""

        insert = True
        i = 0

        while i < len(pdu):

            read = self._connection.read(size[i])

            if pdu[i] == 'pdu':
                try:
                    pdu_type = PDU_TYPE[read]
                except:
                    insert = False
                    break

                size = pdu_type['size']
                pdu = pdu_type['attribute']
                payload = pdu_type['payload']
                i = 0
                continue

            if pdu[i] in payload:
                if pdu[i] == 'endereco':
                    read = read.hex().upper()
                    address = read
                else:
                    read = read.decode('utf-8')

                attributes.append('timestamp')
                values.append(str(datetime.datetime.today())[:19])
                attributes.append(pdu[i])  # tag
                values.append(read)
            i += 1

        if insert:
            reading = '\n'

            for iAttribute, attribute in enumerate(attributes):
                if (attribute == 'timestamp' and self.showTime) or attribute != 'timestamp':
                    reading += f"{attribute}: {values[iAttribute]}\n"
            
            return reading
        
        return ''


