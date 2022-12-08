import serial
from pynmeaparser import NMEAParser

def handler(fields):
    print(fields)

parser = NMEAParser()
parser.add_handler('GPGGA', handler)

with serial.Serial(port='COM21', baudrate=9600, timeout=0) as ser:
    while True:
        try:
            data = ser.readline().decode('utf-8').strip()

            if len(data) > 0:
                parser.process(data)
        except KeyboardInterrupt:
            break
