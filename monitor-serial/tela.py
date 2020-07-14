from main import *
import threading
from serialPort import SerialPort
import serial


class TkSerial:
    # PORTA PROVISÓRIA SERÁ REMOVIDA APÓS A DETECÇÃO AUTOMÁTICA FUNCIONAR
    def __init__(self, root, number, portaProvisoria=''):

        self.serialPort = SerialPort(portaProvisoria)

        # ---- CONNECTION
        self.serialConnection = ''

        # ---- PORT OPTIONS
        self.optPort = ['-']
        self.optVarPort = StringVar(root)
        self.optVarPort.set(self.optPort[0])

        # ---- IMAGES
        self.imgRefresh = PhotoImage(file="img/refresh.png")
        self.imgUpload = PhotoImage(file="img/upload.png")
        self.imgClear = PhotoImage(file="img/clear.png")

        # ---- BAUDRATE OPTIONS
        self.optRate = [
            "9600",
            "57600",
            "115200"
        ]
        self.optVarRate = StringVar(root)
        self.optVarRate.set(self.optRate[0])

        # ---- FRAME
        self.frSerial = Frame(root, bg='white')

        # ---- LABEL
        self.lblSerial = Label(self.frSerial,
                                text=f'SERIAL {number}',
                                font='Verdana',
                                bg='white')

        # ---- SEND
        self.frSend = Frame(self.frSerial)

        self.txtSend = Entry(self.frSend,
                               relief='solid',
                               bg='#FBFBFE',
                               width=56)

        self.btnUpload = Button(self.frSend, image=self.imgUpload, width=34, command=self.send, state=DISABLED)

        self.txtSend.grid(row=0, column=0, padx=1)
        self.btnUpload.grid(row=0, column=1, padx=1)

        # ---- TEXT
        self.frTxt = Frame(self.frSerial, relief='solid', bg='#FBFBFE', highlightbackground="black", highlightthickness=1)

        self.sBar = Scrollbar(self.frTxt)

        self.txtSerial = Text(self.frTxt,
                               relief='flat',
                               bg='#FBFBFE',
                               width=45,
                               height=25,
                               yscrollcommand=self.sBar.set,
                               state=DISABLED)

        self.sBar.grid(row=0, column=1, sticky='NSE')
        self.txtSerial.grid(row=0, column=0)

        self.sBar.config(command=self.txtSerial.yview)

        # ---- CLEAR / SHOW TIMESTAMP
        self.frLiveConfig = Frame(self.frSerial, bg='white')

        self.btnClear = Button(self.frLiveConfig, image=self.imgClear, width=63, height=20, command=self.clear)

        self.showTime = BooleanVar()
        self.showTime.set(True)
        self.chShowTime = Checkbutton(self.frLiveConfig,
                                      text="Show Timestamp",
                                      variable=self.showTime,
                                      font=('Verdana', 10),
                                      bg='white',
                                      command=self.showTimeChange)

        self.chShowTime.pack(side='left')
        self.btnClear.pack(side='right')

        # ---- PORT / BAUDRATE
        self.frConfig = Frame(self.frSerial, bg='white')

        # PORT
        self.frPort = Frame(self.frConfig, bg="white")
        self.lblSerialPort = Label(self.frPort,
                                    text="Port: ",
                                    font=("Verdana", 10),
                                    bg="white")
        self.optSerialPort = OptionMenu(self.frPort, self.optVarPort, *self.optPort)
        self.btnRefreshPorts = Button(self.frPort, image=self.imgRefresh, height=20, width=20,
                                      command=self.releasePorts)
        self.lblSerialPort.grid(row=0, column=0)
        self.optSerialPort.grid(row=0, column=1)
        self.btnRefreshPorts.grid(row=0, column=2)

        # BAUDRATE
        self.frBaudrate = Frame(self.frConfig, bg="white")
        self.lblSerialRate = Label(self.frBaudrate,
                                    text="Baudrate: ",
                                    font=("Verdana", 10),
                                    bg="white")
        self.optSerialRate = OptionMenu(self.frBaudrate, self.optVarRate, *self.optRate)
        self.lblSerialRate.grid(row=0, column=0)
        self.optSerialRate.grid(row=0, column=1)

        # GRID
        self.frBaudrate.pack(side='right')
        self.frPort.pack(side='left')

        # ---- START / STOP
        self.btnSerial = Button(self.frSerial,
                                 text="START",
                                 font=("Verdana", 15),
                                 bg='#B8F8BE',
                                 relief='solid',
                                 padx=20,
                                 pady=5,
                                 command=self.serialStart)

        # ---- GRID
        self.lblSerial.grid(row=0, column=0, pady=35)
        self.frSend.grid(row=1, column=0, pady=3, sticky='W')
        self.frTxt.grid(row=2, column=0)
        self.frLiveConfig.grid(row=3, column=0, pady=5, sticky='WE')
        self.frConfig.grid(row=4, column=0, sticky='WE')
        self.btnSerial.grid(row=5, column=0, pady=30)

        self.releasePorts()

    def connect(self):
        # NÃO PERMITE CRIAR UMA NOVA CONEXÃO SE A CONEXÃO ATUAL ESTIVER ATIVA
        if self.optVarPort.get() != self.serialPort.port or not self.serialConnection.is_open:
            self.serialPort.port = self.optVarPort.get()

            try:
                self.serialConnection = serial.Serial(self.serialPort.port, int(self.optVarRate.get()))
            except Exception as err:
                print(err)

                self.btnSerial['text'] = 'START'
                self.btnSerial['bg'] = '#B8F8BE'
                self.serialPort.flag = False
                self.btnUpload.config(state=DISABLED)
                p = self.serialPort.port
                self.serialPort.port = ''
                popupmsg(f"Couldn't connect to port {p}")

                return False

        return True

    def showTimeChange(self):
        self.serialPort.showTime = self.showTime.get()

    def send(self):
        command = str(self.txtSend.get())

        th = threading.Thread(target=serial_write, args=(self.serialConnection, command))
        th.start()

    def clear(self):
        self.txtSerial.config(state="normal")
        self.txtSerial.delete('1.0', END)
        self.txtSerial.config(state=DISABLED)

    def releasePorts(self):
        ports = SerialPort.serial_ports()

        if len(ports) == 0:
            self.optPort = ['-']
        else:
            self.optPort = ports

            menu = self.optSerialPort["menu"]
            menu.delete(0, "end")
            for opt in self.optPort:
                menu.add_command(label=opt, command=lambda value=opt: self.optVarPort.set(value))

    def serialStart(self):
        if self.serialPort.flag:
            self.btnSerial['text'] = 'START'
            self.btnSerial['bg'] = '#B8F8BE'
            self.serialPort.flag = False
            self.btnUpload.config(state=DISABLED)
            self.serialConnection.close()
        else:
            self.serialPort.flag = True
            self.btnSerial['text'] = 'STOP'
            self.btnSerial['bg'] = '#F8C7C7'
            self.btnUpload.config(state="normal")

            self.clear()

            if self.connect():
                th = threading.Thread(target=serial_read,
                                      args=(self.serialConnection, self.serialPort.flag, self.serialPort.showTime, self.txtSerial))
                th.start()


class Border:
    def __init__(self, root):
        self.frborder = Frame(root,
                                width=1,
                                height=720,
                                bg='black')


class Screen:

        def __init__(self, root):
            self.serial0 = TkSerial(root, '0')
            self.serial1 = TkSerial(root, '1')
            self.serial2 = TkSerial(root, '2')

            self.border01 = Border(root)
            self.border12 = Border(root)

            self.serial0.frSerial.grid(row=0, column=0, padx=13)
            self.border01.frborder.grid(row=0, column=1, padx=12)
            self.serial1.frSerial.grid(row=0, column=2, padx=12)
            self.border12.frborder.grid(row=0, column=3, padx=12)
            self.serial2.frSerial.grid(row=0, column=4, padx=13)


if __name__ == '__main__':
    screen = Tk()
    Screen(screen)
    screen.title("Serial Monitor")
    screen.geometry("1280x720+100+50")
    screen['bg'] = "white"
    screen.resizable(False, False)
    screen.mainloop()
