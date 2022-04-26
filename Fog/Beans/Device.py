from Beans.PayloadAttribute import PayloadAttribute
from Beans.Payload import Payload
from DAOs.PayloadAttributeDAO import PayloadAttributeDAO
from Beans.DeviceType import DeviceType

from datetime import date, datetime

from threading import Thread

import psutil


class Device:
    def __init__(self):
        self.id = -1
        self.address = ''
        self.deviceType = DeviceType()
        self.isReading = False
        self.maxRate = 100

        self.observers = {}

        self.__paDao = PayloadAttributeDAO()
        self.__lastTime = datetime.now()
        self.__packets = 0
        self.__lastRate = 0
        
        self.overLimitCounter = 0

        self.times = []
        self.rates = []

    def toggleMonitoring(self):
        if self.isReading:
            self.isReading = False
            self.__paDao.queue.put((False, False))  # Coloca item falso para parar Thread de inserção do banco

            # TESTE
            arq = open(f"{self.address}.txt", "w")
            for time in self.times:
                arq.write(f"{time}\n")
            for rate in self.rates:
                arq.write(f"{rate}\n")
            arq.close()

        else:
            self.isReading = True
            th_db = Thread(target=self.__paDao.payloadQueueConsumer)    # Thread que insere no banco pela fila
            th_db.start()

        self.observers['deviceStatus'](self)
        self.__lastTime = datetime.now()

    def treat(self, packet):
        if self.isReading:  # Se for pra ler o pacote
            # Instância do payload
            payload = Payload()
            payload.date = datetime.now()
            payload.rate = self.__lastRate

            # Verifica estrutura do pacote
            if packet[0:2] != self.deviceType.byteId or len(packet) != self.deviceType.getLengthAttributes() + 6:
                print("Packet not recognized")
                self.toggleMonitoring()
                return

            self.__packets += 1

            i = 6
            for attribute in self.deviceType.attributes:    # Transforma String packet em objeto Payload
                value = ''
                for _ in range(attribute.size):
                    value += packet[i]
                    i += 1

                payloadAttribute = PayloadAttribute()
                payloadAttribute.attribute = attribute
                payloadAttribute.value = value

                payload.payloadAttributes.append(payloadAttribute)

            # Insere payload na fila de inserção
            self.__paDao.queue.put((self, payload))

            if (datetime.now() - self.__lastTime).seconds >= 1:     # Calcula taxa de pacotes
                self.__lastRate = (self.__packets / 1)
                self.observers['devicePayload'](self.address, payload)    # Emite payload

                self.times.append(datetime.now().strftime('%H:%M:%S'))
                self.rates.append(self.__packets)   # TESTE

                self.__packets = 0

                if int(payload.rate) > int(self.maxRate)*1.01:   # Taxa de pacotes superior ao limite
                    if self.overLimitCounter >= 5:
                        print("Packet rate is over the limit")
                        self.toggleMonitoring()
                        self.overLimitCounter = 0
                        return False
                    else:
                        self.overLimitCounter += 1
                        

                self.__lastTime = datetime.now()

    def getReading(self, fromDate, toDate, attribute):
        if attribute == '0':
            values = self.__paDao.getRates(self, fromDate, toDate)
        else:
            values = self.__paDao.getValues(self, attribute, fromDate, toDate)

        if values is False:
            return False

        valuesList = []
        datesList = []
        for value in values:
            datesList.append(value[1])
            valuesList.append(int(value[0]))

        return {
            'values': valuesList,
            'dates': datesList
        }
