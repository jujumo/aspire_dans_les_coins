__author__ = 'jumo'

import logging

import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from os.path import exists

# using selenium
from selenium import webdriver
persistent_driver = webdriver.Firefox()


def is_url(path):
    url = urlparse(path)
    return bool(url.netloc)


def get_content_url(url, driver=None):
    logging.debug('requesting {}'.format(url))
    # response = urlopen(req)
    _driver = driver or webdriver.Firefox()
    _driver.get(url)
    page_content = _driver.page_source

    if not driver:
        _driver.close()

    return page_content


def get_content_file(filepath):
    logging.debug('opening {}'.format(filepath))
    with open(filepath, 'r', encoding='utf-8') as html_file:
        content = html_file.read()
    return content


def get_content_auto(url):
    if is_url(url):
        return get_content_url(url, persistent_driver)
    elif exists(url):
        return get_content_file(url)


def get_page_tree(url):
    page_content = get_content_auto(url)
    root_page = bs(page_content, 'html5lib')
    return root_page


