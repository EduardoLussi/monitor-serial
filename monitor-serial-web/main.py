from bottle import get, post, run, response
from serialPort import SerialPort
import json

s0 = SerialPort()
s1 = SerialPort()
s2 = SerialPort()


@get('/ports')
def getPorts():
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        res = s0.serial_ports()
        return json.dumps(res)
    except Exception as err:
        print(err)
        return '-'


@get('/start0')
def start0():
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        res = s0.serial_read()
    except Exception as err:
        erro = str(err)
        return erro

    return res

@post('/stop0')
def stop0():
    response.add_header('Access-Control-Allow-Origin', '*')

    s0.disconnect()

@get('/connect0/<port>/<baudrate>')
def connect0(port, baudrate):
    response.add_header('Access-Control-Allow-Origin', '*')
    
    s0.port = str(port)
    s0.baudrate = int(baudrate)

    try:
        res = s0.connect()
        return res
    except Exception as err:
        return err

@post('/send0/<message>')
def send0(message):
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        res = s0.serial_write(message)
    except Exception as err:
        print(err)
        return err



@get('/start1')
def start1():
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        res = s1.serial_read()
    except Exception as err:
        erro = str(err)
        return erro

    return res

@post('/stop1')
def stop1():
    response.add_header('Access-Control-Allow-Origin', '*')

    s1.disconnect()

@get('/connect1/<port>/<baudrate>')
def connect1(port, baudrate):
    response.add_header('Access-Control-Allow-Origin', '*')
    
    s0.port = str(port)
    s0.baudrate = int(baudrate)

    try:
        res = s1.connect()
        return res
    except Exception as err:
        return err
    
@post('/send1/<message>')
def send1(message):
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        res = s1.serial_write(message)
    except Exception as err:
        print(err)
        return err


@get('/start2')
def start2():
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        res = s2.serial_read()
    except Exception as err:
        erro = str(err)
        return erro

    return res

@post('/stop2')
def stop2():
    response.add_header('Access-Control-Allow-Origin', '*')

    s2.disconnect()

@get('/connect2/<port>/<baudrate>')
def connect2(port, baudrate):
    response.add_header('Access-Control-Allow-Origin', '*')
    
    s0.port = str(port)
    s0.baudrate = int(baudrate)

    try:
        res = s2.connect()
        return res
    except Exception as err:
        return err

@post('/send2/<message>')
def send2(message):
    response.add_header('Access-Control-Allow-Origin', '*')

    try:
        res = s2.serial_write(message)
        return res
    except Exception as err:
        print(err)
        return err


run(port=8080)