from sys import platform

from threading import Thread

import glob
import serial

from DAOs.DeviceDAO import DeviceDAO


class SerialPort:
    def __init__(self):
        self.portName = ''
        self.baudRate = 115200
        self._connection = ''
        self.devices = []
        self.isConnected = False
        self.stayConnected = True

        self.thMonitor = ''

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

    def connect(self):
        while self.isConnected is False:
            try:
                self._connection = serial.Serial(self.portName, self.baudRate)
                self.isConnected = True
            except Exception as err:
                print(err)

    def disconnect(self):
        self._connection.close()
        self.isConnected = False

    # def send(self, message):
    #     if self.isConnected:
    #         try:
    #             self._connection.write(bytes(message, 'utf-8'))
    #         except Exception as err:
    #             print(err)
    #             return False
    #         return True
    #     return False

    # def read(self):
    #     if self.isConnected:
    #         while len(self.device.payload) <= 0:
    #             continue
    #         return self.device.payload[-1].toDict()
    #     else:
    #         return False

    def monitor(self):
        # Primeiro pacote da conexão é desconsiderado
        self.connect()
        try:
            self._connection.readline()
        except Exception as err:
            print(err)

        while self.stayConnected:
            self.connect()

            # Leitura do pacote
            try:
                read = self._connection.readline()[:-2]
            except Exception as err:
                print(err)
                continue    # Pacote é desconsiderado se ocorrer erro na leitura
            
            print("Packet received")

            # Identifica byteId e endereço
            byteId = str(hex(read[0]))[2:]
            address = str(hex(read[1]))[2:]
            address += str(hex(read[2]))[2:]

            # Transorma pacote para String
            packet = byteId
            packet += address
            for byte in read[3:]:
                packet += chr(int(hex(byte), 16))

            currentDevice = ''

            # Verifica existência de dispositivo na lista
            deviceFound = False
            for device in self.devices:
                if device.address == address:
                    currentDevice = device
                    deviceFound = True
                    break

            # Caso o dispositivo não estiver na lista, precisa ser identificado
            if deviceFound is False:
                deviceDao = DeviceDAO()
                device = deviceDao.getDevice(byteId, address)   # Busca dispositivo no banco

                if device is False:     # Se o dispositivo não for reconhecido, pacote é desconsiderado
                    print(f"Device {address} not recognized")
                    continue

                print(f"{device.deviceType.name} ({device.address}) found")

                device.observers['deviceStatus'] = self.observers['deviceStatus']
                device.observers['devicePayload'] = self.observers['devicePayload']

                self.devices.append(device)
                self.observers['devices']()     # Emite atualização nos dispositivos
                currentDevice = device

            if currentDevice.treat(packet) is False:   # Dispositivo trata seu pacote
                self._connection.write(bytes(b'b'))
                print("Bloquear")

        self.disconnect()
