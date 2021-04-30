from Utils.DBConnection import Connection

from Beans.Device import Device
from Beans.Attribute import Attribute


class DeviceDAO:
    def __init__(self):
        self.connection = Connection()

    def getAttributes(self, device):
        try:
            self.connection.cursor.execute(f"SELECT Attribute.id, Attribute.name, Attribute.size, Attribute.unit FROM ("
                                           f"((Attribute INNER JOIN PDUAttribute ON Attribute.id = PDUAttribute.Attribute_id)"
                                           f"INNER JOIN PDU ON PDUAttribute.PDU_id = PDU.id)"
                                           f"INNER JOIN Device ON PDU.id = Device.PDU_id) WHERE Device.id = '{str(device.id)}' ORDER BY PDUAttribute.position")
            attrList = self.connection.cursor.fetchall()

            if len(attrList) == 0:
                return False

            attributes = []
            for attr in attrList:
                attribute = Attribute()
                attribute.id = int(attr[0])
                attribute.name = str(attr[1])
                attribute.size = int(attr[2])
                attribute.unit = str(attr[3])

                attributes.append(attribute)

            return attributes

        except Exception as err:
            print(f"Failed to get attributes: \n{err}")
            return False

    def getDevice(self, byteId):
        try:
            self.connection.cursor.execute(f"SELECT * FROM Device WHERE byteId = '{str(byteId)}'")
            deviceList = self.connection.cursor.fetchall()

            if len(deviceList) == 0:
                return False

            device = Device()
            device.id = int(deviceList[0][0])
            device.name = str(deviceList[0][1])
            device.img = str(deviceList[0][2])
            device.byteId = str(deviceList[0][3])

            attributes = self.getAttributes(device)
            if attributes is False:
                return False
            device.attributes = attributes

            return device

        except Exception as err:
            print(f"Failed to select device: \n{err}")
            return False
