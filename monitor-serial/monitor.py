import serial
import datetime
from tkinter import *
from threading import Lock
from tkinter import *


def popupmsg(msg):
    popup = Tk()
    popup.wm_title("ERROR")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10, padx=5)
    B1 = Button(popup, text="OK", command=popup.destroy, width=5)
    B1.pack(pady=10)
    popup.mainloop()


def serial_write(con, command):
    mutex = Lock()
    mutex.acquire()
    try:
        con.write(bytes(command, "utf-8"))
    except Exception as err:
        print(err)
        popupmsg(f"Couldn't send the message")
        return False
    mutex.release()
    return True


def serial_read(con, flag, showTime, txt):
    mutex = Lock()

    while flag:
        mutex.acquire()

        bytesToRead = int(con.inWaiting())
        while bytesToRead == 0:
            bytesToRead = int(con.inWaiting())

        read = con.read(bytesToRead)

        try:
            read = read.decode('utf-8').rstrip('\n')
        except Exception as err:
            print(err)

        mutex.release()

        insert = ''
        if showTime:
            insert += (str(datetime.datetime.today())[:19]) + ' -> ' + read
        else:
            insert += read

        txt.config(state="normal")
        txt.insert(END, insert)
        txt.see("end")
        txt.config(state=DISABLED)

    return True
