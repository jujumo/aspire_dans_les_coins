__author__ = 'jumo'

import logging
import argparse
from grab import grab
from create_immo_requests import create


def main():
    try:
        arg_parser = argparse.ArgumentParser(description='Grab real estate ads and sav into a csv file.')
        arg_parser.add_argument('-v', '--verbose', action='store_true', help='verbose message')
        arg_parser.add_argument('-o', '--output', default='', help='output')
        arg_parser.add_argument('-a', '--append', action='store_true', help='append into csv file if already exists')
        args = arg_parser.parse_args()

        if args.verbose:
            logging.getLogger().setLevel(logging.INFO)
            if __debug__:
                logging.getLogger().setLevel(logging.DEBUG)

        temp_filepath = "requests.txt"
        create(temp_filepath)
        grab(temp_filepath, args.output, args.append)

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise


if __name__ == '__main__':
    main()
