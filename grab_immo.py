__author__ = 'jumo'

import logging
import argparse
import net
import net.parser_leboncoin as lbc
from net.read_net import grab_offer_urls, grab_offer_list
import pandas as pd
import os.path

CSV_SEP = ';'


def grab():
    try:
        parser = argparse.ArgumentParser(description='Grab LeBoncoins real estate ads and sav into a csv file.')
        parser.add_argument('-v', '--verbose', action='store_true', help='verbose message')
        parser.add_argument('-i', '--url', required=True, help='input')
        parser.add_argument('-o', '--output', default='', help='output')
        parser.add_argument('-a', '--append', action='store_true', help='append into csv file if already exists')
        args = parser.parse_args()

        if args.verbose:
            logging.getLogger().setLevel(logging.INFO)
            if __debug__:
                logging.getLogger().setLevel(logging.DEBUG)

        # collect all offers urls
        logging.info('populates ads')
        url_list = grab_offer_urls(args.url, lbc.parse_page_list)
        # collect all offers
        offers = grab_offer_list(url_list, lbc.parse_page_estate)

        # load previous csv id needed
        if args.append and os.path.exists(args.output):
            table = pd.read_csv(args.output, sep=CSV_SEP)
            table = table.set_index('url')
        else:
            table = pd.DataFrame(columns=lbc.SaleEstate.properties_required() + lbc.SaleEstate.properties_optional())
            table = table.set_index('url')

        # and the look for ads details
        logging.info('retreive ads info')
        for offer in offers:
            new_ads = pd.Series(offer.__dict__)
            table.at[offer.url] = new_ads
        # # None instead of Nan
        # table.where(table.notnull(), None)

        # finally: save it
        table.to_csv(args.output, sep=CSV_SEP)

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise


if __name__ == '__main__':
    grab()
