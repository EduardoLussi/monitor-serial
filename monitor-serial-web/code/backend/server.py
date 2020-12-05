from bottle import get, post, run, response

import threading

from Beans.SerialPort import SerialPort
import json

SerialPorts = []
BlackList = []


@get('/devices')
def getDevices():
    response.add_header('Access-Control-Allow-Origin', '*')

    sp = SerialPort()

    ports = sp.getPorts()
    if ports is False or len(ports) == 0:
        return json.dumps({'devices': False})

    devices = []
    SerialPorts.clear()

    for i, portName in enumerate(ports):
        sp = SerialPort()
        sp.portName = portName
        if sp.setDevice():
            sp.id = i
            deviceJson = json.JSONDecoder().decode(json.dumps(sp.device, default=lambda o: o.__dict__))
            devices.append(deviceJson)

            SerialPorts.append(sp)

    return json.dumps({'devices': devices})


@post('/read/<id>/<maxRate>')
def monitor(id, maxRate):
    response.add_header('Access-Control-Allow-Origin', '*')

    sp = ''

    try:
        sp = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return False

    sp.maxReadingRate = int(maxRate)

    th = threading.Thread(target=sp.monitor)

    try:
        th.start()
    except Exception as err:
        print(err)
        return False


@get('/read/<id>')
def read(id):
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        sp = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return json.dumps({'payload': False, 'rate': 0})

    values = sp.read()

    if values is False:
        return json.dumps({'payload': False, 'rate': 0})

    values['rate'] = sp.readingRate

    values = json.dumps(values)

    return values


@get('/send/<id>/<message>')
def send(id, message):
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        sp = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return False

    try:
        res = sp.send(str(message))
    except Exception as err:
        print(err)
        return False

    return json.dumps(res)


@post('/close/<id>')
def close(id):
    response.add_header('Access-Control-Allow-Origin', '*')
    try:
        sp = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return

    try:
        sp.disconnect()
    except Exception as err:
        print(err)


@get('/getValues/<id>/<fromDate>/<toDate>/<attribute>')
def getValues(id, fromDate, toDate, attribute):
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        sp = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return json.dumps({False})

    data = sp.device.getReading(fromDate, toDate, attribute)

    if data is False:
        return json.dumps({False})

    return json.dumps(data)


run(port=8080)
