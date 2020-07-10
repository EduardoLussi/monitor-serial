# TESTE GIT
import serial
from pdu import *
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
        con.write(bytes(command))
    except Exception as err:
        print(err)
        popupmsg(f"Couldn't send the message")
        return False
    mutex.release()
    return True


def serial_read(con, flag, showTime, txt):
    mutex = Lock()

    while flag:
        attributes = []
        values = []

        pdu = PDU_DEFAULT['attribute']

        i = 0

        mutex.acquire()
        while i < len(pdu):

            read = con.read(con.in_waiting)

            attributes.append('data')
            values.append(str(datetime.datetime.today())[:19])

            attributes.append(pdu[i])  # tag
            values.append(read)
            i += 1
        mutex.release()

        txt.config(state="normal")
        for i, attribute in enumerate(attributes):

            if attribute == 'data':
                if showTime:
                    txt.insert(END, f"{values[i]} -> ")
            else:
                txt.insert(END, f"{values[i]}\n")

            txt.see("end")

        txt.config(state=DISABLED)

    return True
