__author__ = 'jumo'

import logging

from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from os.path import exists

# using selenium
from selenium import webdriver
pd = None


class Browser:
    def __init__(self):
        self.driver = None

    def __del__(self):
        if self.driver:
            self.driver.close()

    def get(self, url):
        if not self.driver:
            self.driver = webdriver.Firefox()
        self.driver.get(url)
        page_content = self.driver.page_source  # is already decoded
        return page_content


singleton_browser = Browser()


def is_url(path):
    url = urlparse(path)
    return bool(url.netloc)


def get_content_url(url):
    logging.debug('requesting {}'.format(url))
    page_content = singleton_browser.get(url)
    return page_content


def get_content_file(filepath):
    logging.debug('opening {}'.format(filepath))
    with open(filepath, 'r', encoding='utf-8') as html_file:
        content = html_file.read()
    return content


def write_content_file(filepath, content):
    logging.debug('opening {}'.format(filepath))
    with open(filepath, 'w', encoding='utf-8') as html_file:
        html_file.write(content)


def get_content_auto(url):
    if is_url(url):
        return get_content_url(url)
    elif exists(url):
        return get_content_file(url)


def get_page_tree(url):
    page_content = get_content_auto(url)
    root_page = bs(page_content, 'html5lib')
    return root_page


