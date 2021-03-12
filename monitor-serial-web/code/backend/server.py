from Beans.SerialPort import SerialPort
import json
import threading
from flask import Flask
from flask_cors import cross_origin, CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins='*')
cors = CORS(app, resources={r"/resetDevices": {"origins": "*"},
                            r"/close/*": {"origins": "*"},
                            r"/getValues/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content_Type'

SerialPorts = []


@sio.event
def deviceStatus(id):
    try:
        port = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return False

    sio.emit(f'{id}Status', {'isReading': port.isReading})


@sio.event
def devicePayload(id, payload):
    data = {}
    for payloadAttribute in payload.payloadAttributes:
        data[payloadAttribute.attribute.name] = payloadAttribute.value
    sio.emit(f'{id}Payload', data)


@sio.event
def devices():
    devices = []

    for port in SerialPorts:
        devices.append(port.id)

    sio.emit('devices', devices)


def releasePorts():
    sp = SerialPort()

    ports = sp.getPorts()

    SerialPorts.clear()

    for i, portName in enumerate(ports):
        sp = SerialPort()
        sp.portName = portName
        if sp.setDevice():
            sp.id = i
            sp.observers['deviceStatus'] = deviceStatus
            sp.observers['devicePayload'] = devicePayload
            sp.observers['sio'] = sio
            SerialPorts.append(sp)

    devices()


releasePorts()


@app.route('/resetDevices', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def resetDevices():
    releasePorts()
    devices()
    print(SerialPorts)
    return 'ok'


@app.route('/read/<id>/<maxRate>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def monitor(id, maxRate):
    sp = ''

    try:
        sp = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return False

    sp.maxReadingRate = int(maxRate)
    print("monitoring")
    sio.start_background_task(target=sp.monitor)
    # th = threading.Thread(target=sp.monitor)
    #
    # try:
    #     th.start()
    # except Exception as err:
    #     print(err)
    #     return False

    return 'ok'


@app.route('/close/<id>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def close(id):

    try:
        sp = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return

    try:
        sp.disconnect()
    except Exception as err:
        print(err)

    return 'ok'


@app.route('/devices', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def devicesReq():
    devices = []

    for port in SerialPorts:
        devices.append(port.id)

    return json.dumps(devices)


@app.route('/device/<id>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def deviceConfig(id):
    try:
        port = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return False

    device = {
        'name': port.device.name,
        'img': port.device.img,
        'attributes': []
    }
    for attribute in port.device.attributes:
        device['attributes'].append({
            'id': attribute.id,
            'name': attribute.name,
            'unit': attribute.unit
        })

    return json.dumps({'device': device, 'isReading': port.isReading})


@app.route('/getValues/<id>/<fromDate>/<toDate>/<attribute>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def getValues(id, fromDate, toDate, attribute):
    try:
        sp = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return json.dumps({False})

    data = sp.device.getReading(fromDate, toDate, attribute)
    if data is False:
        return json.dumps({False})

    return json.dumps(data)


# @sio.event
# def connect():
#     print('connect')
#
#
# @sio.event
# def disconnect():
#     print('disconnect')


if __name__ == '__main__':
    sio.run(app, port=8080)
