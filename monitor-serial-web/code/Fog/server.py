from Beans.SerialPort import SerialPort
#from Simulation.SerialPort import SerialPort
import json
from threading import Thread
from flask import Flask
from flask_cors import cross_origin, CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)

sio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')
cors = CORS(app, resources={r"/resetDevices": {"origins": "*"},
                            r"/close/*": {"origins": "*"},
                            r"/getValues/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content_Type'

SerialPorts = []


@sio.event
def deviceStatus(device):
    sio.emit(f'{device.address}Status', {'isReading': device.isReading, 'maxRate': device.maxRate})
    return


@sio.event
def devicePayload(address, payload):
    data = {}
    data['rate'] = payload.rate
    for payloadAttribute in payload.payloadAttributes:
        data[payloadAttribute.attribute.name] = payloadAttribute.value
    sio.emit(f'{address}Payload', data)


@sio.event
def devices():
    devicesList = []
    for sp in SerialPorts:
        for device in sp.devices:
            devicesList.append(device.address)

    sio.emit('devices', devicesList)


def releasePorts():
    for sp in SerialPorts:
        sp.stayConnected = False
        sp.thMonitor.join()

    SerialPorts.clear()

    sp = SerialPort()
    ports = sp.getPorts()
    for portName in ports:
        sp = SerialPort()
        sp.portName = portName
        sp.thMonitor = Thread(target=sp.monitor)
        sp.observers['devices'] = devices
        sp.observers['deviceStatus'] = deviceStatus
        sp.observers['devicePayload'] = devicePayload
        SerialPorts.append(sp)
        sp.thMonitor.start()


@app.route('/resetDevices', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def resetDevices():
    releasePorts()
    devices()
    print(SerialPorts)
    return 'ok'


@app.route('/read/<address>/<maxRate>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def monitor(address, maxRate):
    for sp in SerialPorts:
        for device in sp.devices:
            if device.address == address:
                device.maxRate = maxRate
                device.toggleMonitoring()
    return 'ok'


@app.route('/close/<address>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def close(address):
    for sp in SerialPorts:
        for device in sp.devices:
            if device.address == address:
                device.toggleMonitoring()
    return 'ok'


@app.route('/devices', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def devicesReq():
    devicesList = []
    for sp in SerialPorts:
        for device in sp.devices:
            devicesList.append(device.address)

    return json.dumps(devicesList)


@app.route('/device/<address>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def deviceConfig(address):
    for sp in SerialPorts:
        for device in sp.devices:
            if device.address == address:
                deviceJ = {
                    'name': device.deviceType.name,
                    'img': device.deviceType.img,
                    'attributes': []
                }
                for attribute in device.deviceType.attributes:
                    deviceJ['attributes'].append({
                        'id': attribute.id,
                        'name': attribute.name,
                        'unit': attribute.unit
                    })

                return json.dumps({'device': deviceJ, 'isReading': device.isReading, 'maxRate': device.maxRate})

    return json.dumps({'device': {}, 'isReading': False})


@app.route('/getValues/<address>/<fromDate>/<toDate>/<attribute>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def getValues(address, fromDate, toDate, attribute):
    for sp in SerialPorts:
        for device in sp.devices:
            if device.address == address:
                data = device.getReading(fromDate, toDate, attribute)
                if data is False:
                    return json.dumps({False})
                return json.dumps(data)

    return json.dumps(False)


if __name__ == '__main__':
    sio.run(app, port=8080, debug=True)
