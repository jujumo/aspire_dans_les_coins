__author__ = 'jumo'

import logging
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from os.path import exists


def is_url(path):
    url = urlparse(path)
    return bool(url.netloc)


def get_content_url(url):
    logging.debug('requesting {}'.format(url))
    response = urlopen(url)
    mybytes = response.read()
    page_content = mybytes.decode("latin-1")
    response.close()
    return page_content


def get_content_file(filepath):
    logging.debug('opening {}'.format(filepath))
    with open(filepath, 'r', encoding='utf-8') as html_file:
        content = html_file.read()
    return content


def get_content_auto(url):
    if is_url(url):
        return get_content_url(url)
    elif exists(url):
        return get_content_file(url)


def get_page_tree(url):
    page_content = get_content_auto(url)
    root_page = bs(page_content, 'html5lib')
    return root_page

