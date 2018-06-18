__author__ = 'jumo'

import logging
from urllib.request import urlopen
from urllib.parse import urlparse


def get_page_content(url):
    logging.debug('requesting {}'.format(url))
    response = urlopen(url)
    mybytes = response.read()
    page_content = mybytes.decode("latin-1")
    response.close()
    return page_content


def is_url(path):
    url = urlparse(path)
    return bool(url.netloc)


def grab_offer_urls(url, offers_list_parser):
    url_list = list()
    while url:
        page_content = get_page_content(url)
        page_list = offers_list_parser(page_content, url)
        url = page_list.next_url
        url_list.extend(page_list.url_list)
    return url_list


def grab_offer_list(url_list, offers_parser):
    offers = []
    for url in url_list:
        logging.debug('retreive ad info {}'.format(url))
        page_content = get_page_content(url)
        offer = offers_parser(page_content, url)
        offers.append(offer)
    return offers
