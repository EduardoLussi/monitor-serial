from Utils.DBConnection import Connection

from Beans.Device import Device
from Beans.DeviceType import DeviceType
from Beans.Attribute import Attribute


class DeviceDAO:
    def __init__(self):
        self.connection = Connection()

    def getAttributes(self, byteId):
        try:
            self.connection.cursor.execute(f"SELECT Attribute.id, Attribute.name, Attribute.size, Attribute.unit FROM ("
                                           f"((Attribute INNER JOIN PDUAttribute ON Attribute.id = PDUAttribute.Attribute_id) "
                                           f"INNER JOIN PDU ON PDUAttribute.PDU_id = PDU.id) "
                                           f"INNER JOIN DeviceType ON PDU.id = DeviceType.PDU_id) WHERE DeviceType.byteId = '{str(byteId)}' "
                                           f"ORDER BY PDUAttribute.position")
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

    def getDevice(self, byteId, address):
        try:
            # Procura por dispositivos com byteId e endereço
            self.connection.cursor.execute(f"SELECT Device.id, name, img FROM DeviceType "
                                           f"INNER JOIN Device ON DeviceType.id = Device.DeviceType_id "
                                           f"WHERE DeviceType.byteId = {byteId} AND Device.address = '{address}'")
            deviceList = self.connection.cursor.fetchall()

            if len(deviceList) == 0:    # Nenhum dispositivo encontrado
                return False

            # Define deviceType
            deviceType = DeviceType()
            deviceType.byteId = byteId
            deviceType.name = str(deviceList[0][1])
            deviceType.img = str(deviceList[0][2])

            # Encontra atributos de deviceType
            attributes = self.getAttributes(deviceType.byteId)
            if attributes is False:     # Nenhum atributo encontrado para o dispositivo
                return False
            deviceType.attributes = attributes

            # Define o dispositivo
            device = Device()
            device.id = int(deviceList[0][0])
            device.address = address
            device.deviceType = deviceType

            return device

        except Exception as err:
            print(f"Failed to select device: \n{err}")
            return False
