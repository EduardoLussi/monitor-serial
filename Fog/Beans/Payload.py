class Payload:
    def __init__(self):
        self.date = ''
        self.rate = 0
        self.payloadAttributes = []

    def toDict(self):
        payload = {
            'payload': self.attributesToDict()
        }

        payload['payload']['date'] = str(self.date)
        payload['payload']['rate'] = str(self.rate)

        return payload

    def attributesToDict(self):
        dict = {}
        for payloadAttribute in self.payloadAttributes:
            dict[payloadAttribute.attribute.name] = payloadAttribute.value
        return dict
