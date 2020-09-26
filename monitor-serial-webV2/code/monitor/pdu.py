# --------------------------------
#     PDU DESCRIPTION
# --------------------------------
# forma de organizacao do pacote, criar um novo

PDU_DEFAULT = {
    'attribute': ['pdu'],
    'size': [1],
    'payload': [],
    'length': 1
}

PDU_INCENDIO = {
    'attribute': ['endereco', 'umidade', 'temperatura', 'gas', 'chamas'],
    'size': [2, 2, 2, 2, 1],
    'payload': ['endereco', 'umidade', 'temperatura', 'gas', 'chamas'],
    'length': 9
}

PDU_RFID = {
    'attribute': ['tag'],
    'size': [8],
    'payload': ['tag'],
    'length': 9
}

PDU_ALIMENTACAO = {
    'attribute': ['tag'],
    'size': [8],
    'payload': ['tag'],
    'length': 9
}

PDU_AGUA = {
    'attribute': ['tag'],
    'size': [8],
    'payload': ['tag'],
    'length': 9
}

PDU_TYPE = {
    b'\x11': PDU_INCENDIO,
    b'\x12': PDU_RFID,
    b'\x13': PDU_ALIMENTACAO,
    b'\x14': PDU_AGUA
}

# Descrição dispositivos


FIRE_ALARM = {
    'name': 'Fire Alarm',
    'img': 'fire-alarm.png',
    'pduType': PDU_INCENDIO
}

RFID = {
    'name': 'RFID',
    'img': 'rfid.png',
    'pduType': PDU_RFID
}

PETS_WATER = {
    'name': 'Pets Water',
    'img': 'bowl.png',
    'pduType': PDU_ALIMENTACAO
}

WATER = {
    'name': 'Water Metering',
    'img': 'pipe.png',
    'pduType': PDU_AGUA
}

DEVICE_TYPE = {
    b'\x11': FIRE_ALARM,
    b'\x12': RFID,
    b'\x13': PETS_WATER,
    b'\x14': WATER
}