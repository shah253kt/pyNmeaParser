# pyNMEAParser
A package to parse general form of NMEA sentences. It is not specific to just certain devices only.
After successfully parsing an NMEA data, it will return a list of fields in the NMEA sentence.

# Installation
Checkout [PyPi Homepage](https://pypi.org/project/pynmeaparser/) as well.
```
pip install pynmeaparser
```

# API
## `NMEAParser()`
**Description:** The constructor for NMEAParser class.

**Returns:** NMEAParser object.

```python
# Import package
from pynmeaparser import NMEAParser

# Create NMEAParser object
parser = NMEAParser()
```
---
## `add_handler(id:str, fn:Callable)`
**Description:** Attach a handler function to be called when `id` matches the key.

**Parameters:**

`id`: A string representing the key.

`fn`: The handler function of which will be called if `id` matches the key. The function needs to accept a list as a parameter.

```python
def my_handler(fields):
    print(fields)


parser.add_handler('GPGGA', my_handler)
```
---
## `process(sentence:str)`
**Description:** Process the string passed to the function. This string will be concatenated with the previously incomplete processed string.

**Parameters:**

`sentence`: NMEA string format. This can be an arbitrary data, but needs to adhere to NMEA standard.
```python
# Process an NMEA string
parser.process('$GPZDA,024008.97,24,11,2022,00,00*62')
parser.process('$MY_OWN,SOME,DATA,HERE*2F') # Can be arbitrary as long as adhering to NMEA standard.
```
---
## `get_buffer()`
**Description:** Process the string passed to the function. This string will be concatenated with the previously incomplete processed string.

**Returns:** The string currently in the buffer.

```python
print('Unprocessed string:', parser.get_buffer()) # Display the string that is still not processed.
```

# Examples
## Simple parse

```python
from pynmeaparser import NMEAParser

def my_handler(fields):
    print(fields)

parser = NMEAParser() # Create parser object
parser.add_handler('GPZDA', handler) # Add handler. The handler function will be called if the first field contains the key.
parser.process('$GPZDA,024008.97,24,11,2022,00,00*62') # Process NMEA string here.
# Output: ['GPZDA', '024008.97', '24', '11', '2022', '00', '00']
```

## Parse from file
```python
from pynmeaparser import NMEAParser

def handler(fields):
    global parsed
    print(fields)
    parsed += 1

parser = NMEAParser()
parser.add_handler('GPGGA', handler)
parser.add_handler('AIVDM', handler)
parser.add_handler('GPVTG', handler)
parser.add_handler('GPZDA', handler)
parser.add_handler('GPGLL', handler)
parser.add_handler('GPRMC', handler)

with open('sample_data.txt') as f:
    for line in f.readlines():
        print(line)
        parser.process(line)

print('\nLines in sample file: {}\nSuccessfully parsed: {}'.format(lines, parsed))
```

## Parse from serial port
This example makes use of [PySerial](https://pypi.org/project/pyserial/).
```python
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
```