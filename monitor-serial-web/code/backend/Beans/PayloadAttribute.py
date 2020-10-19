from Beans.Attribute import Attribute


class PayloadAttribute:
    def __init__(self):
        self.attribute = Attribute()
        self.value = ''

    def toDict(self):
        payloadAttr = {
            self.attribute.name: self.value
        }

        return payloadAttr
