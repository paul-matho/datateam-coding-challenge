""" Series of basic utilities """
import os
import json
import csv
import random
import string
import struct
import logging
import datetime

logger = logging.getLogger(__name__)


def configure_logging():
    today_time = datetime.datetime.now().strftime('%d-%m-%Y %I%M%S')
    logfilepath = os.getcwd() + '\\logs\\'
    logfilename = str(today_time) + '.log'
    os.makedirs(logfilepath, mode=0o777, exist_ok=True)

    handlers = [logging.FileHandler(logfilepath+logfilename), logging.StreamHandler()]

    logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        level=logging.DEBUG,
                        handlers=handlers)


class FileGenerator(object):
    def __init__(self):
        self.spec = self.read_spec()

    def read_spec(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + "\\fixed-width\\spec.json") as json_data:
            data = json.load(json_data)
            for k, v in data.items():
                if ',' in v:
                    data[k] = tuple(v.split(','))
            data['FormatString'] = ' '.join('{}{}'.format(fw, 's') for fw in data["Offsets"])
            data['FieldStruct'] = struct.Struct(data['FormatString'])
            return data


class FixedWidthFileGenerator(FileGenerator):
    def __init__(self, filename, num_of_rows=100):
        super().__init__()
        self.filename = filename
        self.num_of_rows = num_of_rows

    def generate_fw_file(self):
        try:
            logger.info('Generating fixed width file. Filename: ' + self.filename)
            fw_file = open(self.filename, "wb")
        except:
            logger.warning('Invalid filename provided.')
            return

        for i in range(self.num_of_rows):
            row = ""
            for offset in self.spec['Offsets']:
                chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(0, int(offset))))
                chars = chars.ljust(int(offset))
                row += chars
            row = row + '\n'
            fw_file.write(row.encode(self.spec['InputEncoding']))
        fw_file.close()
        logger.info('Fixed width file "' + self.filename + '" successfully created.')


class FixedWidthFileParser(FileGenerator):
    def __init__(self, input_file):
        super().__init__()
        self.input_file = input_file
        self.output_file = input_file[:-4] + '.csv'

    def parse_file(self):
        try:
            input_file = os.getcwd() + "\\" + self.input_file
            fw_file = open(input_file, "r", encoding=self.spec['InputEncoding'])
        except:
            logger.warning('Could not open inputfile.')
            return

        with open(self.output_file, "w", newline='\n', encoding=self.spec['OutputEncoding']) as csv_file:
            wr = csv.writer(csv_file)
            if self.spec["IncludeHeader"] == "True":
                wr.writerow(self.spec["ColumnNames"])
            for line in fw_file:
                fields = self.spec['FieldStruct'].unpack_from(bytes(line.encode(self.spec['InputEncoding'])))
                fields = [str(item, self.spec['OutputEncoding']).strip() for item in fields]
                wr.writerow(fields)
        fw_file.close()
        csv_file.close()
        logger.info('CSV file "' + self.output_file + '" successfully created.')
