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

stop = True
def test():
    import psutil
    from time import sleep
    from datetime import datetime
    now_list = []
    percent = []
    pcks = []
    while stop:
        now = datetime.now().time()
        pr = psutil.cpu_percent()
        print(f"{now} {pr}")
        now_list.append(str(now).replace('.', ','))
        percent.append(str(pr).replace('.', ','))
        pcks.append(SerialPorts[0].readingRate)
        sleep(1)
    arquivo = open("cpu.txt", "a")
    for now in now_list:
        arquivo.writelines(f"{now}\n")
    for pr in percent:
        arquivo.writelines(f"{pr}\n")
    for rate in pcks:
        arquivo.writelines(f"{rate}\n")

th = Thread(target=test)
@sio.event
def deviceStatus(id):
    for port in SerialPorts:
        if port.id == int(id):
            sio.emit(f'{id}Status', {'isReading': port.isReading, 'maxRate': port.maxReadingRate, 'rate': port.readingRate})
            return


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
        sp.observers['deviceStatus'] = deviceStatus
        sp.observers['devicePayload'] = devicePayload
        sp.observers['sio'] = sio
        if sp.setDevice():
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
    for port in SerialPorts:
        if port.id == int(id):
            port.maxReadingRate = int(maxRate)
            sio.start_background_task(target=port.monitor)
            break
    #th.start()
    return 'ok'


@app.route('/close/<id>', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def close(id):
    for port in SerialPorts:
        if port.id == int(id):
            try:
                port.disconnect()
            except Exception as err:
                print(err)
            break
    global stop
    stop = False
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
    for port in SerialPorts:
        if port.id == int(id):
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

            return json.dumps({'device': device, 'isReading': port.isReading, 'rate': port.maxReadingRate})

    return json.dumps({'device': {}, 'isReading': False})


@app.route('/getValues/<id>/<fromDate>/<toDate>/<attribute>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def getValues(id, fromDate, toDate, attribute):
    for port in SerialPorts:
        if port.id == int(id):
            data = port.device.getReading(fromDate, toDate, attribute)
            if data is False:
                return json.dumps({False})
            return json.dumps(data)
    return json.dumps(False)


if __name__ == '__main__':
    sio.run(app, port=8080, debug=True)
