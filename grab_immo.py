__author__ = 'jumo'

import logging
import argparse
import ads
from ads.net import get_page_tree, is_url
from ads.parsing import ParserCollection, ParseResult
import pandas as pd
import os.path

CSV_SEP = ';'


def grab():
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

        # collect all offers urls
        logging.info('collecting ads')
        parsed = ParseResult()

        if is_url(args.input):
            # a single url
            parsed.add_url(args.input)
        elif os.path.exists(args.input):
            # its a file
            with open(args.input) as f:
                urls = set(f.readlines())
                parsed.add_url(urls)

        while parsed.urls:
            source_url = parsed.urls.pop()
            root_page = get_page_tree(source_url)
            parsed.update(ParserCollection.parse(root_page, source_url))

        # load previous csv id needed
        if args.append and os.path.exists(args.output):
            table = pd.read_csv(args.output, sep=CSV_SEP)
            table = table.set_index('url')
        else:
            table = pd.DataFrame(columns=ads.ads.SaleEstate.properties_required()
                                         + ads.ads.SaleEstate.properties_optional()
                                         + ['url'])
            table = table.set_index('url')

        # and the look for ads details
        logging.info('retreive ads info')
        for source_url, offer in parsed.ads.items():
            new_ads = pd.Series(offer.__dict__)
            table.at[source_url] = new_ads
        # None instead of Nan
        table.where(table.notnull(), None)

        # finally: save it
        table.to_csv(args.output, sep=CSV_SEP)

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise


if __name__ == '__main__':
    grab()
