class Payload:
    def __init__(self):
        self.date = ''
        self.payloadAttributes = []

    def toDict(self):
        payload = {
            'payload': self.attributesToDict()
        }

        payload['payload']['date'] = str(self.date)

        return payload

    def attributesToDict(self):
        dict = {}
        for payloadAttribute in self.payloadAttributes:
            dict[payloadAttribute.attribute.name] = payloadAttribute.value
        return dict
