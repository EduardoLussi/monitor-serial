from bottle import get, post, run, response, route
from serialPort import SerialPort
import json
from pdu import *

# devicesDev = []
# serialPortsDev = [
#     SerialPort(),
#     SerialPort(),
#     SerialPort(),
#     SerialPort()
# ]

serialPorts = []

# for key, val in DEVICE_TYPE.items():
#     devicesDev.append(DEVICE_TYPE[key])

@get('/ports')
# def getPortsDev():
#     response.add_header('Access-Control-Allow-Origin', '*')

#     return json.dumps(devicesDev)
def getPorts():
    releasePorts()

    devices = []
    for port in serialPorts:
        devices.append(port.device)

    return json.dumps(devices)


def releasePorts():
    sp = SerialPort()

    try:
        res = sp.serial_ports()
    except Exception as err:
        print(err)
        return

    serialPorts.clear()

    for portName in res:
        port = SerialPort()
        port.port = portName
        try:
            port.setDevice()
        except Exception as err:
            print(err)
            continue

        serialPorts.append(port)


@get('/start/<id>')
def start(id):
    response.add_header('Access-Control-Allow-Origin', '*')
    
    try:
        res = serialPorts[int(id)].serial_read()
    except Exception as err:
        print(err)
        return json.dumps({
            'data': False
        })

    return json.dumps({
        'data': res
    })

@post('/stop/<id>')
def stop(id):
    response.add_header('Access-Control-Allow-Origin', '*')

    serialPorts[int(id)].disconnect()

# @get('/connect0/<port>/<baudrate>')
# def connect0(port, baudrate):
#     response.add_header('Access-Control-Allow-Origin', '*')
    
#     s0.port = str(port)
#     s0.baudrate = int(baudrate)

#     try:
#         res = s0.connect()
#         return res
#     except Exception as err:
#         return err

# @post('/send/<idDevice>/<message>')
# def send0(message):
#     response.add_header('Access-Control-Allow-Origin', '*')

#     try:
#         res = s0.serial_write(message)
#     except Exception as err:
#         print(err)
#         return err

# @post('/showTimestamp/<idDevice>')
# def showTimestamp():
#     response.add_header('Access-Control-Allow-Origin', '*')

#     if s0.showTime:
#         s0.showTime = False
#     else: 
#         s0.showTime = True
    
#     return ''

run(port=8080)