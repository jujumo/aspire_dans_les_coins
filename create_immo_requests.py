__author__ = 'jumo'


import argparse
import logging


# https://www.leboncoin.fr/recherche/?category=9&region=22&cities=38190&real_estate_type=1,2,3,4,5&square=30-300&price=25000-250000&rooms=1-8
request_format = 'https://www.leboncoin.fr/recherche/?' \
                 'category={category}&region={region}&cities={cities}&real_estate_type={real_estate_type}&' \
                 'square={min_sqrt}-{max_sqrt}&price={min_price}-{max_price}&rooms={min_room}-{max_room}'


def create(output_filepath):
    # collect all offers urls
    critrium = dict(
        category=9,
        region=22,
        cities=38000,
        real_estate_type=1,
        min_sqrt='min',
        max_sqrt='max',
        min_price='min',
        max_price='max',
        min_room='min',
        max_room='max',
    )

    # adjust
    # critrium['min_sqrt'] = 130
    # critrium['max_price'] = 600000

    city_list = [38190, 38240, 38420, 38330, 38610, 38700, 38410]
    with open(output_filepath, 'w') as f:
        for critrium['cities'] in city_list:
            f.write(request_format.format(**critrium) + '\n')


def main():
    try:
        arg_parser = argparse.ArgumentParser(description='Grab real estate ads and sav into a csv file.')
        arg_parser.add_argument('-v', '--verbose', action='store_true', help='verbose message')
        # arg_parser.add_argument('-i', '--input', required=True, help='input can be either a file or an url')
        arg_parser.add_argument('-o', '--output', default='requests.txt', help='output')
        args = arg_parser.parse_args()

        if args.verbose:
            logging.getLogger().setLevel(logging.INFO)
            if __debug__:
                logging.getLogger().setLevel(logging.DEBUG)

        create(args.output)

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise


if __name__ == '__main__':
    main()
