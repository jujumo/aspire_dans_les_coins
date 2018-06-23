__author__ = 'jumo'

import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


def get_page_tree(url):
    logging.debug('requesting {}'.format(url))
    response = urlopen(url)
    mybytes = response.read()
    page_content = mybytes.decode("latin-1")
    response.close()
    root_page = bs(page_content, 'html5lib')
    return root_page
