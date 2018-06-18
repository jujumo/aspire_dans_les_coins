__author__ = 'jumo'

from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from ads.ads import SaleEstate, OffersList
from datetime import datetime


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


def parse_page_estate(page_content, url):
    page_root = bs(page_content, 'html5lib')
    info = parse_page_estate_to_dict(page_root, url)
    estate = SaleEstate(**info)
    return estate


def parse_page_list(page_content, url):
    page_root = bs(page_content, 'html5lib')
    page_content = page_root.find('section', class_='tabsContent')

    # list all ads in the page
    links_tree = page_content.find_all('a')
    new_urls = (l['href']for l in links_tree)
    new_urls = map(nice_url, new_urls)
    url_list = []
    url_list.extend(new_urls)

    # recurse on next pages
    pagination_div = page_root.find('div', class_='pagination_links_container')
    next_page_url = None
    if pagination_div:
        next_button = pagination_div.find('a', {'id': 'next'})
        if next_button:
            next_page_url = nice_url(next_button['href'])

    sales = OffersList(url, url_list=url_list, next_url=next_page_url)
    return sales


def is_leboncoin(path):
    url = urlparse(path)
    return bool(url.netloc == 'www.leboncoin.fr')


def is_leboncoin_list(path):
    url = urlparse(path)
    return bool(url.netloc == 'www.leboncoin.fr')