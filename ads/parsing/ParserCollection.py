__author__ = 'jumo'

from bs4 import BeautifulSoup as bs
import logging


class ParserCollection(type):
    """
    collects all parsers, and use them all to parse.
    Through metaclass, this is called for each class Parser* definition .
    """
    parser_list = []

    def __new__(mcs, name, bases, dct):
        parser = type.__new__(mcs, name, bases, dct)
        """ add every parser (except base class) to the collection """
        if not name == 'ParseResult':
            # ParserImpl is base class, do not do that
            ParserCollection.parser_list.append(parser)
        return parser

    @classmethod
    def parse(cls, root_page, source_url):
        assert(type(root_page) is bs)
        result = ParseResult()
        logging.debug(f'try parse {source_url} :')
        for dedicated_parser in cls.parser_list:
            dedicated_parsed = dedicated_parser.parse(root_page, source_url)
            if not dedicated_parsed.is_empty():
                logging.debug('is {}'.format(dedicated_parser.__name__))
                result.update(dedicated_parsed)
        return result


class ParseResult(metaclass=ParserCollection):
    """ the base class of all parsers,
    a parser definition automatically trigger ParserCollection.__new__ and thus matinaint the collection upt to date.
    """
    def __init__(self, ads=None, urls=None):
        self.urls = urls or set()
        self.ads = ads or dict()

    @classmethod
    def parse(cls, root_page, source_url):
        result = cls()
        return result

    def add_url(self, url):
        if type(url) is str:
            self.urls.add(url)
        else:
            self.urls.update(url)

    def update(self, other):
        assert(type(other.urls) == set)
        assert (type(self.urls) == set)
        self.urls.update(other.urls)
        self.ads.update(other.ads)

    def is_empty(self):
        empty_urls = not self.urls
        empty_ads = not self.ads
        return empty_urls and empty_ads