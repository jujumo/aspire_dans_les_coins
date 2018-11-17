__author__ = 'jumo'

import logging
import argparse
import matplotlib.pyplot as plt
from ads.io import from_csv_to_pandas


CSV_SEP = ';'


def graph_viz():
    try:
        arg_parser = argparse.ArgumentParser(description='Graph visualize real estate ads.')
        arg_parser.add_argument('-v', '--verbose', action='store_true', help='verbose message')
        arg_parser.add_argument('-i', '--input', required=True, help='input can be either a file or an url')
        args = arg_parser.parse_args()

        if args.verbose:
            logging.getLogger().setLevel(logging.INFO)
            if __debug__:
                logging.getLogger().setLevel(logging.DEBUG)

        # load previous csv id needed
        df = from_csv_to_pandas(args.input)

        category_name = 'zip'
        categories = set(df[category_name].values)
        # fig, ax = plt.subplots()
        for i, category in enumerate(categories):
            view = df[df[category_name] == category]
            plt.subplot(7,1,i+1)
            prix = view['price'].values / view['surface'].values
            surf = view['surface'].values
            plt.plot(surf, prix, '.')
            # plt.scatter(view['surface'], view['price'], label=category)


        plt.show()

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise


if __name__ == '__main__':
    graph_viz()
