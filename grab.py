__author__ = 'jumo'

import logging
import argparse
import ads.io
from ads.net import get_page_tree, is_url
from ads.parsing.ParserCollection import ParserCollection, ParseResult
import os.path


def grab(input_filpath, output_filepath, append=False):
    # collect all offers urls
    logging.info('collecting ads')
    parsed = ParseResult()

    if is_url(input_filpath):
        # a single url
        parsed.add_url(input_filpath)
    elif os.path.exists(input_filpath):
        # its a file
        with open(input_filpath) as f:
            urls = set(l.strip() for l in f.readlines())
            parsed.add_url(urls)

    while parsed.urls:
        source_url = parsed.urls.pop()
        logging.info(f'loading {source_url}')
        root_page = get_page_tree(source_url)
        parsed.update(ParserCollection.parse(root_page, source_url))

    # TODO: load previous csv id needed
    ads.io.to_csv(output_filepath, parsed.ads)


def main_grab():
    try:
        arg_parser = argparse.ArgumentParser(description='Grab real estate ads and sav into a csv file.')
        arg_parser.add_argument('-v', '--verbose', action='count', default=0, help='verbose message')
        arg_parser.add_argument('-i', '--input', required=True, help='input can be either a file or an url')
        arg_parser.add_argument('-o', '--output', default='', help='output')
        arg_parser.add_argument('-a', '--append', action='store_true', help='append into csv file if already exists')
        args = arg_parser.parse_args()

        if args.verbose:
            logging.getLogger().setLevel(logging.INFO)
        if args.verbose > 1:
            logging.getLogger().setLevel(logging.DEBUG)

        grab(args.input, args.output, args.append)

    except Exception as e:
        logging.critical(e)
        if args.verbose > 1:
            raise


if __name__ == '__main__':
    main_grab()
