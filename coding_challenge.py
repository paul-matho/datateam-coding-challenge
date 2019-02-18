from utils import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    """ Simple script used to create a sample fixed width text file which is then
     parsed into csv format"""

    configure_logging()

    filename = "fixed_width_file.txt"
    logger.info('Script started.')

    fixed_width_file_generator = FixedWidthFileGenerator(filename)
    fixed_width_file_parser = FixedWidthFileParser(filename)

    fixed_width_file_generator.generate_fw_file()
    fixed_width_file_parser.parse_file()


if __name__ == '__main__':
    main()
