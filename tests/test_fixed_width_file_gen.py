import unittest
import os
import datetime
import glob
import csv
from utils import *


def generate_files():
    today_time = datetime.datetime.now().strftime('%d-%m-%Y-%I%M%S')
    filename = str(today_time) + "_fw_file.txt"
    fixed_width_file_generator = FixedWidthFileGenerator(filename, num_of_rows=5)
    fixed_width_file_parser = FixedWidthFileParser(filename)
    fixed_width_file_generator.generate_fw_file()
    fixed_width_file_parser.parse_file()
    return fixed_width_file_generator, fixed_width_file_parser


class TestFixedWidthFileGenerator(unittest.TestCase):
    fw, fp = generate_files()

    def test_fixed_width_file_gen(self):
        """ Test that the fixed width file is generated. """
        fw, fp = generate_files()
        text_files = glob.glob(os.path.join(os.getcwd() + "\\", '*.txt'))
        output_files = [file for file in text_files if fw.filename in file]
        self.assertTrue(output_files)

    def test_fixed_width_row_length(self):
        """ Tests the length of each row in the fixed width file. """
        fw, fp = generate_files()
        fw_file = open(fw.filename, "r", encoding=fw.spec['InputEncoding'])
        failures = 0
        for line in fw_file:
            if len(line) != fw.spec['FieldStruct'].size+1:                  # account for '\n'
                failures += 1
        fw_file.close()
        self.assertEqual(0, failures)

    def test_csv_file_gen(self):
        """ Test that the csv file is generated. """
        fw, fp = generate_files()
        text_files = glob.glob(os.path.join(os.getcwd() + "\\", '*.csv'))
        output_files = [file for file in text_files if fp.output_file in file]
        self.assertTrue(output_files)

    def test_items_in_first_row_csv(self):
        """ Check that the first row of the csv file matches first row of the fixed width file. """
        fw, fp = generate_files()
        fw_file = open(fw.filename, "r", encoding=fw.spec['InputEncoding'])
        with open(fp.output_file) as f:
            csv_f = csv.reader(f)
            if fp.spec["IncludeHeader"] == "True":
                next(csv_f)
                csv_row = next(csv_f)
                csv_row = list(filter(None, csv_row))
            for line in fw_file:
                fw_row = fw.spec['FieldStruct'].unpack_from(bytes(line.encode(fw.spec['InputEncoding'])))
                fw_row = [str(item, fw.spec['OutputEncoding']).strip() for item in fw_row]
                fw_row = list(filter(None, fw_row))
                break
        fw_file.close()
        f.close()
        result = list(set(fw_row) & set(csv_row))
        if len(csv_row) == len(result) & len(fw_row) == len(result):
            result = 1
        else:
            result = 0
        self.assertEqual(1, result)


if __name__ == '__main__':
    unittest.main()
