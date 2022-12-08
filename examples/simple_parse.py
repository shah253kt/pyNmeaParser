from pynmeaparser import NMEAParser

parsed = 0

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

lines = 0

with open('sample_data.txt') as f:
    for line in f.readlines():
        lines += 1
        print(line)
        parser.process(line)

print('\nLines in sample file: {}\nSuccessfully parsed: {}\n{}'.format(lines, parsed, 'All tests passed' if lines == parsed else 'Some tests failed'))