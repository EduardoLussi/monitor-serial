from Utils.DBConnection import Connection
from datetime import datetime
from queue import Queue


class PayloadAttributeDAO:
    def __init__(self):
        self.connection = Connection()
        self.queue = Queue()

    def payloadQueueConsumer(self):
        lastTime = datetime.now()
        # Listas para formação das queries de inserção dos payloads
        devices = []
        payloads = []
        while True:
            device, payload = self.queue.get()

            if device is False or payload is False:
                break

            devices.append(device)
            payloads.append(payload)

            # print(f"Inserindo em {device.deviceType.name} -> {payload.payloadAttributes[0].attribute.name}: {payload.payloadAttributes[0].value}")
            # print(f"Tamanho da fila: {self.queue.qsize()}")

            if (datetime.now() - lastTime).seconds >= 5:    # Realiza inserção no banco a cada 5 segundos
                self.insertPayload(devices, payloads)
                lastTime = datetime.now()
                devices.clear()
                payloads.clear()

        print("Payload db consumer finished")
        self.insertPayload(devices, payloads)

    # Realiza a inserção de vários payloads
    def insertPayload(self, devices, payloads):
        # Cria query de inserção dos payloads
        queryPayload = 'INSERT INTO Payload (Device_id, timestamp, rate) VALUES '
        for i, payload in enumerate(payloads):
            queryPayload += f"({devices[i].id}, {payload.date.timestamp()}, {payload.rate}), "
        queryPayload = queryPayload[:-2] + ';'

        with self.connection.lock:  # Realiza a inserção dos payloads
            try:
                self.connection.cursor.execute(queryPayload)
            except Exception as err:
                print(f"Failed to insert payload:\n{err}")
                return False

        # Adiciona os ids dos payloads inseridos na lista
        payloadIdList = []
        for i, payload in enumerate(payloads):
            try:
                self.connection.cursor.execute(f"SELECT id from Payload WHERE Device_id = {devices[i].id} "
                                               f"AND timestamp = {payload.date.timestamp()};")
            except Exception as err:
                print(f"Failed to select id from Payload:\n{err}")

            payloadIdList.append(self.connection.cursor.fetchall()[0][0])

        # Cria query de inserção em PayloadAttribute
        queryPayloadAttr = f'INSERT INTO PayloadAttribute (Payload_id, Attribute_id, value) VALUES '
        for i, payload in enumerate(payloads):
            for payloadAttr in payload.payloadAttributes:
                queryPayloadAttr += f"({payloadIdList[i]}, {payloadAttr.attribute.id}, '{payloadAttr.value}'), "
        queryPayloadAttr = queryPayloadAttr[0:-2] + ';'

        # Realiza inserção em PayloadAttribute
        with self.connection.lock:
            try:
                self.connection.cursor.execute(queryPayloadAttr)
            except Exception as err:
                print(f"Failed to insert in PayloadAttribute:\n{err}")
                return False

        self.commitDB()
        return True

    def getRates(self, device, fromDate, toDate):
        fromDate = datetime.strptime(fromDate, "%Y-%m-%d %H:%M:%S").timestamp()
        toDate = datetime.strptime(toDate, "%Y-%m-%d %H:%M:%S").timestamp()

        sql = f"SELECT Payload.rate, Payload.timestamp FROM PayloadAttribute " \
            f"INNER JOIN Payload ON PayloadAttribute.Payload_id = Payload.id " \
            f"WHERE Device_id = {device.id} AND Payload.timestamp > {fromDate} AND Payload.timestamp < {toDate}"

        try:
            self.connection.cursor.execute(sql)
            data = self.connection.cursor.fetchall()
        except Exception as err:
            print(f"Failed to get rates: \n{err}")
            return False

        if len(data) == 0:
            return False

        return data

    def getValues(self, device, attribute, fromDate, toDate):
        fromDate = datetime.strptime(fromDate, "%Y-%m-%d %H:%M:%S").timestamp()
        toDate = datetime.strptime(toDate, "%Y-%m-%d %H:%M:%S").timestamp()

        sql = f"SELECT value, timestamp FROM PayloadAttribute " \
            f"INNER JOIN Payload ON PayloadAttribute.Payload_id = Payload.id " \
            f"WHERE Device_id = {device.id} AND Attribute_id = {attribute} " \
            f"AND Payload.timestamp > {fromDate} AND Payload.timestamp < {toDate}"

        try:
            self.connection.cursor.execute(sql)
            data = self.connection.cursor.fetchall()
        except Exception as err:
            print(f"Failed to get values: \n{err}")
            return False

        if len(data) == 0:
            return False

        return data

    def commitDB(self):
        with self.connection.lock:
            self.connection.banco.commit()
