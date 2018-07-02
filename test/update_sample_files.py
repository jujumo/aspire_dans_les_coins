#!/usr/bin/env python3
import logging
from ads.net import get_content_url
from os.path import join, realpath, dirname


samples = {
    'sample_annonce_list_nopage.html': 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=38190&real_estate_type=1&price=min-600000&rooms=4-max&square=130-max',
    'sample_annonce_list_pagination.html': 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=Grenoble_38000',
    'sample_annonce_list_last.html': 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=38190&page=8',
    'sample_annonce_estate.html': 'https://www.leboncoin.fr/ventes_immobilieres/1415286514.htm/',
}

SCRIPT_PATH = dirname(realpath(__file__))


def sibling(filename):
    return join(SCRIPT_PATH, filename)


def main():
    try:
        logging.getLogger().setLevel(logging.INFO)
        for filename, url in samples.items():
            content = get_content_url(url)
            filepath = sibling(filename)
            logging.info(f'making {filepath} from {url}')
            with open(filepath, 'w', encoding='utf-8') as fout:
                fout.write(content)

    except Exception as e:
        logging.critical(e)
        if __debug__:
            raise


if __name__ == '__main__':
    main()
