from Utils.DBConnection import Connection
from datetime import datetime


class PayloadAttributeDAO:
    def __init__(self):
        self.connection = Connection()

    def insertPayload(self, device, payload):
        try:
            self.connection.cursor.execute(f"INSERT INTO Payload (Device_id, timestamp) VALUES ({str(device.id)}, "
                                           f"{payload.date.timestamp()});")

            self.connection.cursor.execute(f"SELECT id from Payload WHERE Device_id = {str(device.id)} "
                                           f"AND timestamp = {str(payload.date.timestamp())};")
            payloadId = self.connection.cursor.fetchall()[0][0]

            for payloadAttribute in payload.payloadAttributes:
                self.connection.cursor.execute(f"INSERT INTO PayloadAttribute (Payload_id, Attribute_id, value) "
                                               f"VALUES ({str(payloadId)}, {str(payloadAttribute.attribute.id)}, "
                                               f"'{str(payloadAttribute.value)}');")
            return True

        except Exception as err:
            print(f"Failed to insert payload: \n{err}")
            return False

    def getValues(self, device, attribute, fromDate, toDate):
        fromDate = datetime.strptime(fromDate, "%Y-%m-%d %H:%M:%S").timestamp()
        toDate = datetime.strptime(toDate, "%Y-%m-%d %H:%M:%S").timestamp()

        try:
            sql = f"SELECT value, timestamp FROM PayloadAttribute INNER JOIN Payload ON PayloadAttribute.Payload_id = Payload.id " \
                  f"WHERE Device_id = {device.id} AND Attribute_id = {attribute} " \
                  f"AND Payload.timestamp > {fromDate} AND Payload.timestamp < {toDate}"

            self.connection.cursor.execute(sql)
            data = self.connection.cursor.fetchall()

            if len(data) == 0:
                return False

            return data

        except Exception as err:
            print(f"Failed to get values: \n{err}")
            return False

    def commitDB(self):
        self.connection.banco.commit()
