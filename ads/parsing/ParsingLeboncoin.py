__author__ = 'jumo'

from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from ads.ads import SaleEstate
from datetime import datetime
from .ParsingAll import ParseResult
from os.path import splitext


def nice_url(url):
    return 'https:' + url if url.startswith('//') else url


data_signature = {
    'title': {'data-qa-id': "adview_title"},
    'price': {'data-qa-id': 'adview_price'},
    'date': {'data-qa-id': 'adview_date'},
    'category': {'data-qa-id': 'criteria_item_real_estate_type'},
    'surface': {'data-qa-id': 'criteria_item_square'},
    'rooms': {'data-qa-id': 'criteria_item_rooms'},
    'location': {'data-qa-id': 'adview_location_informations'},
    'real_estate': {'data-qa-id': 'storebox_title'},
}


def parse_page_to_dict(page_root, url):
    info = {'url': url}
    # title
    title_tree = page_root.find('div', data_signature['title'])
    info['title'] = title_tree.contents[0].contents[0].contents[0]

    # date of grabbing (now)
    info['date_grabbed'] = datetime.now()

    # date creation
    date_tree = page_root.find('div', data_signature['date'])
    date = date_tree.contents[0]  # = '13/06/2018 à 17h01'
    info['date_creation'] = date.split()[0]

    # price
    price_tree = page_root.find('div', data_signature['price'])
    price = (price_tree.contents[0].contents[0].contents[1])
    info['price'] = int(price.replace(" ", ""))

    # localization
    location_tree = page_root.find('div', data_signature['location'])
    info['location'] = location_tree.contents[0].contents[1]
    # zip
    info['zip'] = int(location_tree.contents[0].contents[7])

    return info


def parse_page_estate_to_dict(page_root, url):
    # retreive generic infos
    info = parse_page_to_dict(page_root, url)

    # category
    category_tree = page_root.find('div', data_signature['category'])
    category = category_tree.contents[0].contents[1].contents[0]
    info['category'] = category.lower()

    # surface
    surface_tree = page_root.find('div', data_signature['surface'])
    surface = surface_tree.contents[0].contents[1].contents[0]
    info['surface'] = int(surface.split(' ')[0])

    # rooms
    rooms_tree = page_root.find('div', data_signature['rooms'])
    if rooms_tree:
        rooms = rooms_tree.contents[0].contents[1].contents[0]
        info['rooms'] = int(rooms)

    # real estate
    real_estate_tree = page_root.find('span', data_signature['real_estate'])
    if real_estate_tree:
        info['real_estate'] = real_estate_tree.contents[0]

    return info


class ParsingLeboncoinList(ParseResult):
    @classmethod
    def url_match(cls, source_url):
        url = urlparse(source_url)
        is_leboncoin = bool(url.netloc == 'www.leboncoin.fr')
        is_offer = 'offres' in url.path.split('/')
        return is_leboncoin and is_offer

    @classmethod
    def parse(cls, root_page, source_url):
        result = ParseResult()
        # need to fail fast
        if not cls.url_match(source_url):
            return result

        section_content = root_page.find('section', class_='tabsContent')
        if not section_content:
            return result

        # list all ads in the page
        links_tree = section_content.find_all('a')
        new_urls = (l['href'] for l in links_tree)
        new_urls = list(map(nice_url, new_urls))
        result.add_url(new_urls)

        # recurse on next pages by adding nexyt page to the one to process
        pagination_div = root_page.find('div', class_='pagination_links_container')
        if pagination_div:
            next_button = pagination_div.find('a', {'id': 'next'})
            if next_button:
                result.add_url(nice_url(next_button['href']))

        return result


class ParsingLeboncoinAd(ParseResult):
    @classmethod
    def url_match(cls, source_url):
        url = urlparse(source_url)
        is_leboncoin = bool(url.netloc == 'www.leboncoin.fr')
        is_digit = (splitext(url.path.split('/')[-1])[0]).isdigit()
        return False
        return is_leboncoin and is_digit

    @classmethod
    def parse(cls, root_page, source_url):
        result = ParseResult()
        return result
        # need to fail fast
        if not cls.url_match(source_url):
            return result

        info = {}
        # title
        title_tree = root_page.find('div', data_signature['title'])
        info['title'] = title_tree.contents[0].contents[0].contents[0]

        # date of grabbing (now)
        info['date_grabbed'] = datetime.now()

        # date creation
        date_tree = root_page.find('div', data_signature['date'])
        date = date_tree.contents[0]  # = '13/06/2018 à 17h01'
        info['date_creation'] = date.split()[0]

        # price
        price_tree = root_page.find('div', data_signature['price'])
        price = (price_tree.contents[0].contents[0].contents[1])
        info['price'] = int(price.replace(" ", ""))

        # localization
        location_tree = root_page.find('div', data_signature['location'])
        info['location'] = location_tree.contents[0].contents[1]
        # zip
        info['zip'] = int(location_tree.contents[0].contents[7])

        # sale = SaleEstate(**info)
        # result.ads[source_url] = sale

        return result


class ParsingLeboncoinAdEstate(ParseResult):
    @classmethod
    def url_match(cls, source_url):
        url = urlparse(source_url)
        is_leboncoin = bool(url.netloc == 'www.leboncoin.fr')
        is_digit = (splitext(url.path.split('/')[-1])[0]).isdigit()
        is_estate = (url.path.split('/')[1]) == 'ventes_immobilieres'
        return is_leboncoin and is_digit and is_estate

    @classmethod
    def parse(cls, root_page, source_url):
        result = ParseResult()
        # need to fail fast
        if not cls.url_match(source_url):
            return result

        info = {}
        # title
        title_tree = root_page.find('div', data_signature['title'])
        if not title_tree:
            return result
        info['title'] = title_tree.contents[0].contents[0].contents[0]

        # date of grabbing (now)
        info['date_grabbed'] = datetime.now()

        # date creation
        date_tree = root_page.find('div', data_signature['date'])
        date = date_tree.contents[0]  # = '13/06/2018 à 17h01'
        info['date_creation'] = date.split()[0]

        # price
        price_tree = root_page.find('div', data_signature['price'])
        price = (price_tree.contents[0].contents[0].contents[1])
        info['price'] = int(price.replace(" ", ""))

        # localization
        location_tree = root_page.find('div', data_signature['location'])
        info['location'] = location_tree.contents[0].contents[1]
        # zip
        info['zip'] = int(location_tree.contents[0].contents[7])

        # category
        category_tree = root_page.find('div', data_signature['category'])
        category = category_tree.contents[0].contents[1].contents[0]
        info['category'] = category.lower()

        # surface
        surface_tree = root_page.find('div', data_signature['surface'])
        surface = surface_tree.contents[0].contents[1].contents[0]
        info['surface'] = int(surface.split(' ')[0])

        # rooms
        rooms_tree = root_page.find('div', data_signature['rooms'])
        if rooms_tree:
            rooms = rooms_tree.contents[0].contents[1].contents[0]
            info['rooms'] = int(rooms)

        # real estate
        real_estate_tree = root_page.find('span', data_signature['real_estate'])
        if real_estate_tree:
            info['real_estate'] = real_estate_tree.contents[0]

        sale = SaleEstate(**info)
        result.ads[source_url] = sale

        return result
