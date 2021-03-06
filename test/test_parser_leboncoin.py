import unittest
import ads.parsing.ParsingLeboncoin as lbc
from ads.net import get_page_tree


class TestParserLeboncoinList(unittest.TestCase):
    def test_parse_page_list_url(self):
        fake_url = 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=38420&real_estate_type=1&square=130-max&rooms=4-max&price=min-600000'
        result = lbc.ParsingLeboncoinList.url_match(fake_url)
        self.assertEqual(result, True)

    def test_parse_page_list_single(self):
        fake_url = 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=38420&real_estate_type=1&square=130-max&rooms=4-max&price=min-600000'
        fake_filepath = 'sample_annonce_list_nopage.html'
        root_page = get_page_tree(fake_filepath)

        result = lbc.ParsingLeboncoinList.parse(root_page, fake_url)
        urls = sorted(result.urls)

        self.assertEqual(17, len(urls))
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1321296674.htm/', urls[0])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1459715477.htm/', urls[-1])

    def test_parse_page_list_pages(self):
        fake_url = 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=Grenoble_38000'
        fake_filepath = 'sample_annonce_list_pagination.html'
        root_page = get_page_tree(fake_filepath)

        result = lbc.ParsingLeboncoinList.parse(root_page, fake_url)
        urls = sorted(result.urls)

        self.assertEqual(36, len(urls))
        self.assertEqual('https://www.leboncoin.fr/recherche/?category=9&region=22&cities=Grenoble_38000&page=2', urls[0])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1169971633.htm/', urls[1])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1459720545.htm/', urls[-1])

    def test_parse_page_list_last(self):
        fake_url = 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=38190&page=8'
        fake_filepath = 'sample_annonce_list_last.html'
        root_page = get_page_tree(fake_filepath)

        result = lbc.ParsingLeboncoinList.parse(root_page, fake_url)
        urls = sorted(result.urls)

        self.assertEqual(24, len(urls))
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1120473631.htm/', urls[0])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1434440981.htm/', urls[-1])


class TestParserLeboncoin(unittest.TestCase):
    def test_parse_page_info(self):
        fake_url = 'https://www.leboncoin.fr/ventes_immobilieres/1415286514.htm/'
        fake_filepath = 'sample_annonce_estate.html'
        root_page = get_page_tree(fake_filepath)
        result = lbc.ParsingLeboncoinAdEstate.parse(root_page, fake_url)

        self.assertEqual(0, len(result.urls))
        self.assertEqual(1, len(result.ads))
        for id, ad in result.ads.items(): pass
        self.assertEqual(1415286514, id)
        self.assertEqual(fake_url, ad.url)
        self.assertEqual('01/06/2018', ad.date_creation)
        self.assertEqual(495000, ad.price)
        self.assertEqual('maison', ad.real_estate_category)
        self.assertEqual(149, ad.surface)
        self.assertEqual(7, ad.rooms)
        self.assertEqual('https://img7.leboncoin.fr/ad-image/b5b2e7e3ba3d3aa0cc4f807fa74e400ea8a8a14e.jpg', ad.thumb)
        self.assertEqual('Le Versoud', ad.location)
        self.assertEqual('CHRISTIAN JOUTY IMMOBILIER', ad.real_estate_agent)


if __name__ == '__main__':
    unittest.main()

