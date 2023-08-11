from dataclasses import dataclass
from typing import Callable

START_OF_ENCAPSULATION_SENTENCE_DELIMITER = '!'
START_DELIMITER = '$'
FIELD_DELIMITER = ','
CHECKSUM_DELIMITER = '*'

# Exceptions
class ChecksumError(Exception):
    def __init__(self, calculated:int, received:int):
        super().__init__('Checksum mismatch. Should be {:02X} but received {:02X} instead.'.format(calculated, received))


@dataclass
class Handler:
    id:str
    fn:Callable


class NMEAParser:
    def __init__(self):
        self.raise_exceptions = False
        self.sentence = ''
        self.handlers = []


    def process(self, sentence:str, debug:bool = False) -> list:
        '''
        The library should be able to handle misformed statement as well as well formed ones.
        $GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D\r\n
        $GPGGA,184353.07,1929.045,S,0
        2410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D\r\n
        $GPGG$GPGGA,184353.07,1929.0
        !AIVDM,1,1,,A,14eG;o@034o8sd<L9i:a;WF>062D,0*7D
        '''
        
        start_delimiter = None
        self.sentence += sentence.strip()
        self.debug_output = []

        if debug:
            self.debug_output.append(f'[NMEAParser::process()] Current sentence: {sentence}')
            self.debug_output.append(f'[NMEAParser::process()] Sentence: {self.sentence}')

        # Determine which start delimiter is received
        for delimiter in [START_OF_ENCAPSULATION_SENTENCE_DELIMITER, START_DELIMITER]:
            if delimiter in self.sentence:
                start_delimiter = delimiter
                break

        if start_delimiter is None:
            return self.debug_output

        # Remove incomplete preceeding sentences if any
        self.sentence = self.sentence[self.sentence.index(start_delimiter):]

        # Check if checksum delimiter is in the sentence
        if CHECKSUM_DELIMITER not in self.sentence:
            return self.debug_output

        checksum_delimiter_index = self.sentence.index(CHECKSUM_DELIMITER)

        # Check if checksum part is available
        if len(self.sentence) < checksum_delimiter_index + 3:
            return self.debug_output

        end_of_sentence_index = checksum_delimiter_index + 3

        if debug:
            self.debug_output.append(f'[NMEAParser::process()] Cleaned sentence: {self.sentence}')

        # Calculate the checksum received
        try:
            checksum_value = int(self.sentence[checksum_delimiter_index + 1 : end_of_sentence_index], 16)
        except ValueError:
            self.sentence = self.sentence[checksum_delimiter_index:] # Remove the bad part for next cycle
            return self.debug_output

        current_sentence = self.sentence[1:checksum_delimiter_index]
        calculated_checksum = 0

        for c in current_sentence:
            calculated_checksum ^= ord(c)

        # Compare checksum values
        if calculated_checksum != checksum_value and self.raise_exceptions:
            if debug:
                self.debug_output.append(f'[NMEAParser::process()] Invalid checksum [calculated={calculated_checksum} checksum={checksum_value}]')
            raise ChecksumError(calculated_checksum, checksum_value)

        fields = current_sentence.split(FIELD_DELIMITER)

        # Go through all of the handlers and execute those with the same ID
        for handler in self.handlers:
            if handler.id == fields[0]:
                handler.fn(fields)

                if debug:
                    self.debug_output.append(f'[NMEAParser::process()] Found handler: [handler={fields[0]}')

        # Remove processed sentence
        self.sentence = self.sentence[end_of_sentence_index + 1:]

        if debug:
            self.debug_output.append(f'[NMEAParser::process()] Remaining sentence: {self.sentence}')
        
        return self.debug_output


    def get_buffer(self) -> str:
        return self.sentence


    def add_handler(self, id:str, fn:Callable):
        self.handlers.append(Handler(id, fn))
