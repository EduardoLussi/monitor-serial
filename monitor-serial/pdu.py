PDU_DEFAULT = {
    'attribute': ['pdu'],
    'size': [3],
    'payload': [],
    'length': 1
}

PDU_FIRE_ALARM = {
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

PDU_TYPE = {
    b'\x11': PDU_FIRE_ALARM,
    b'\x12': PDU_RFID
}