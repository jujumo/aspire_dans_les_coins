__author__ = 'jumo'

import logging
import argparse
import ads.ads as ads
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

    # load previous csv id needed
    df = ads.to_pandas(parsed.ads)
    if append and os.path.exists(output_filepath):
        old_df = ads.from_csv_to_pandas(output_filepath)
        df.update(old_df)
    ads.from_pandas_to_csv(output_filepath, df)


def main_grab():
    try:
        arg_parser = argparse.ArgumentParser(description='Grab real estate ads and sav into a csv file.')
        arg_parser.add_argument('-v', '--verbose', action='store_true', help='verbose message')
        arg_parser.add_argument('-i', '--input', required=True, help='input can be either a file or an url')
        arg_parser.add_argument('-o', '--output', default='', help='output')
        arg_parser.add_argument('-a', '--append', action='store_true', help='append into csv file if already exists')
        args = arg_parser.parse_args()

        if args.verbose:
            logging.getLogger().setLevel(logging.INFO)
            if __debug__:
                logging.getLogger().setLevel(logging.DEBUG)

        grab(args.input, args.output, args.append)

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise


if __name__ == '__main__':
    main_grab()
