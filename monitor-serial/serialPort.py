import sys
import glob
import serial
from threading import Lock
from tkinter import *
import datetime


def popupmsg(msg):
    popup = Tk()
    popup.wm_title("ERROR")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10, padx=5)
    B1 = Button(popup, text="OK", command=popup.destroy, width=5)
    B1.pack(pady=10)
    popup.mainloop()


class SerialPort:
    def __init__(self):
        self.isReading = False
        self.port = 'COM3'
        self.baudrate = 115200
        self.showTime = True
        self._connection = ''

    @staticmethod
    def serial_ports():
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
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
            popupmsg(f"Couldn't connect to port {self.port}")
            return False
        self.isReading = True
        return True

    def disconnect(self):
        if self._connection != '':
            self._connection.close()
        self.isReading = False

    def serial_write(self, command):
        mutex = Lock()
        mutex.acquire()
        try:
            self._connection.write(bytes(command, "utf-8"))
        except Exception as err:
            print(err)
            popupmsg(f"Couldn't send the message")
            return False
        mutex.release()
        return True

    def serial_read(self, txt):
        mutex = Lock()

        while self.isReading:
            mutex.acquire()

            bytesToRead = int(self._connection.inWaiting())
            while bytesToRead == 0:
                bytesToRead = int(self._connection.inWaiting())

            read = self._connection.read(bytesToRead)

            try:
                read = read.decode('utf-8').rstrip('\n')
            except Exception as err:
                print(err)

            mutex.release()

            insert = ''
            if self.showTime:
                insert += (str(datetime.datetime.today())[:19]) + ' -> ' + read
            else:
                insert += read

            txt.config(state="normal")
            txt.insert(END, insert)
            txt.see("end")
            txt.config(state=DISABLED)

        return True
