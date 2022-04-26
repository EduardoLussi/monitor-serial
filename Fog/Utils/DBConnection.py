import sqlite3

from threading import Lock


class Connection:

    __instance = None

    def __new__(cls):
        if Connection.__instance is None:
            Connection.__instance = object.__new__(cls)

            try:
                Connection.__instance.banco = sqlite3.connect('data.db', check_same_thread=False)
                Connection.__instance.cursor = Connection.__instance.banco.cursor()
            except sqlite3.Error as err:
                print(err)

            # cls.createDatabase()

        return Connection.__instance

    def __init__(self):
        self.lock = Lock()

    @staticmethod
    def createDatabase():
        try:
            Connection.__instance.cursor.execute("CREATE TABLE IF NOT EXISTS PDU ("
                                                 "id INTEGER PRIMARY KEY AUTOINCREMENT);")

            Connection.__instance.cursor.execute("CREATE TABLE IF NOT EXISTS Attribute ("
                                                 "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                 "name TEXT,"
                                                 "size INTEGER);")

            Connection.__instance.cursor.execute("CREATE TABLE IF NOT EXISTS Device ("
                                                 "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                                 "name TEXT, "
                                                 "img TEXT, "
                                                 "byteId TEXT, "
                                                 "PDU_id INTEGER,"
                                                 "FOREIGN KEY (PDU_id) REFERENCES PDU (id));")

            Connection.__instance.cursor.execute("CREATE TABLE IF NOT EXISTS PDUAttribute ("
                                                 "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                 "PDU_id INTEGER,"
                                                 "Attribute_id INTEGER,"
                                                 "FOREIGN KEY (PDU_id) REFERENCES PDU (id),"
                                                 "FOREIGN KEY (Attribute_id) REFERENCES Attribute (id));")

            Connection.__instance.cursor.execute("CREATE TABLE IF NOT EXISTS Payload ("
                                                "id	INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                "Device_id INTEGER,"
                                                "data TEXT,"
                                                "FOREIGN KEY(Device_id) REFERENCES Device (id));")

            Connection.__instance.cursor.execute("CREATE TABLE IF NOT EXISTS PayloadAttribute ("
                                                 "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                 "Payload_id INTEGER,"
                                                 "Attribute_id INTEGER,"
                                                 "FOREIGN KEY(Payload_id) REFERENCES Payload (id),"
                                                 "FOREIGN KEY(Attribute_id) REFERENCES Attribute (id));")

            Connection.__instance.banco.commit()
        except sqlite3.Error as err:
            print(err)
