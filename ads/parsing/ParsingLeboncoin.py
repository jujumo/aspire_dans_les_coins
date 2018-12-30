__author__ = 'jumo'


from urllib.parse import urlparse
from ads.ads import SaleEstate
from datetime import datetime
from .ParserCollection import ParseResult
from os.path import splitext


def nice_url(_url):
    url = urlparse(_url)
    if not url.netloc:
        # relative path -> make it absolute
        url = url._replace(scheme='https', netloc='www.leboncoin.fr')
    return url.geturl()


data_signature = {
    'application': ['div', {'id': 'application'}],
    'list_panel': ['div', {'role': 'tabpanel'}],
    'list_next': ['div', {'role': 'tabpanel'}],
    'title': {'data-qa-id': "adview_title"},
    'price': {'data-qa-id': 'adview_price'},
    'date': {'data-qa-id': 'adview_date'},
    'image': {'data-qa-id': 'slideshow_container'},
    'description': {'data-qa-id': 'adview_description_container'},
    'real_estate_category': {'data-qa-id': 'criteria_item_real_estate_type'},
    'surface': {'data-qa-id': 'criteria_item_square'},
    'rooms': {'data-qa-id': 'criteria_item_rooms'},
    'location': {'data-qa-id': 'adview_location_informations'},
    'real_estate_agent': {'data-qa-id': 'storebox_title'},
}


class ParsingLeboncoinList(ParseResult):
    @classmethod
    def url_match(cls, source_url):
        url = urlparse(source_url)
        is_leboncoin = bool(url.netloc == 'www.leboncoin.fr')
        is_list = 'recherche' in url.path.split('/')
        return is_leboncoin and is_list

    @classmethod
    def parse(cls, root_page, source_url):
        result = ParseResult()
        # need to fail fast
        if not cls.url_match(source_url):
            return result

        section_content = root_page.find(*data_signature['application'])
        if not section_content:
            return result

        # list all ads in the page
        links_tree = section_content.find_all('li', {'itemtype': 'http://schema.org/Offer'})
        new_urls = (l.find('a') for l in links_tree)
        new_urls = (l['href'] for l in new_urls)
        new_urls = list(map(nice_url, new_urls))
        result.add_url(new_urls)

        # recurse on next pages by adding next page to the one to process
        nav_bars = root_page.find_all('nav')
        if nav_bars and len(nav_bars) == 3:
            page_bar = nav_bars[-1]
            for page_last in page_bar.find_all('li'): pass
            next = page_last.a
            if next and next['href']:
                result.add_url(nice_url(next['href']))

        return result


class ParsingLeboncoinAdEstate(ParseResult):
    @classmethod
    def url_match(cls, source_url):
        url = urlparse(source_url)
        is_leboncoin = bool(url.netloc == 'www.leboncoin.fr')
        is_digit = (splitext(url.path.split('/')[2])[0]).isdigit()
        is_estate = (url.path.split('/')[1]) == 'ventes_immobilieres'
        return is_leboncoin and is_digit and is_estate

    @classmethod
    def parse(cls, root_page, source_url):
        result = ParseResult()
        # need to fail fast
        if not cls.url_match(source_url):
            return result

        info = dict()

        # create an ID
        urlp = urlparse(source_url)
        id = int(urlp.path.split('/')[-2].split('.')[0])

        info['url'] = source_url

        # title
        title_tree = root_page.find('div', data_signature['title'])
        if not title_tree:
            return result
        info['title'] = title_tree.contents[0].contents[0].contents[0]

        # description
        description_tree = root_page.find('div', data_signature['description'])
        if not description_tree:
            return result
        description = description_tree.contents[0].contents[0].contents
        description = [d for d in description if not str(d).startswith('<')]
        description = ' / '.join(description)
        info['description'] = description

        # date of grabbing (now)
        info['date_grabbed'] = datetime.now()

        # date creation
        date_tree = root_page.find('div', data_signature['date'])
        if not date_tree:
            return result
        date = date_tree.contents[0]  # = '13/06/2018 à 17h01'
        info['date_creation'] = date.split()[0]

        # price
        price_tree = root_page.find('div', data_signature['price'])
        if not price_tree:
            return result
        price = (price_tree.contents[0].contents[0].contents[1])
        info['price'] = int(price.replace(" ", ""))

        # localization
        location_tree = root_page.find('div', data_signature['location'])
        if not location_tree:
            return result
        currated_location_fields = (l.strip() for l in location_tree.contents[0].contents)
        currated_location_fields = [l for l in currated_location_fields if l and 'react-text' not in l]
        if currated_location_fields:
            info['location'] = currated_location_fields[0]
        # zip
        if len(currated_location_fields) == 1:
            info['zip'] = int(currated_location_fields[0])
        else:
            info['zip'] = int(currated_location_fields[1])

        # category
        category_tree = root_page.find('div', data_signature['real_estate_category'])
        if location_tree:
            category = category_tree.contents[0].contents[1].contents[0]
            info['real_estate_category'] = category.lower()
        else:
            info['real_estate_category'] = 'estate'

        # surface
        surface_tree = root_page.find('div', data_signature['surface'])
        if not surface_tree:
            return result
        surface = surface_tree.contents[0].contents[1].contents[0]
        info['surface'] = int(surface.split(' ')[0])

        # rooms
        rooms_tree = root_page.find('div', data_signature['rooms'])
        if rooms_tree:
            rooms = rooms_tree.contents[0].contents[1].contents[0]
            info['rooms'] = int(rooms)

        # images
        images_tree = root_page.find('div', data_signature['image'])
        if images_tree:
            info['thumb'] = images_tree.find('img')['src']

        # real estate
        real_estate_tree = root_page.find('span', data_signature['real_estate_agent'])
        if real_estate_tree:
            info['real_estate_agent'] = real_estate_tree.contents[0]

        sale = SaleEstate(**info)
        result.ads[id] = sale

        return result
