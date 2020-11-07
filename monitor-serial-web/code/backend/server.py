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


@post('/read/<id>')
def monitor(id):
    response.add_header('Access-Control-Allow-Origin', '*')


    try:
        sp = SerialPorts[int(id)]
    except Exception as err:
        print(err)
        return

    th = threading.Thread(target=sp.monitor)

    try:
        th.start()
    except Exception as err:
        print(err)


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


run(port=8080)
