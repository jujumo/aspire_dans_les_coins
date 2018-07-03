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

        self.assertEqual(19, len(urls))
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1321296674.htm/', urls[0])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1455670832.htm/', urls[-1])

    def test_parse_page_list_pages(self):
        fake_url = 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=Grenoble_38000'
        fake_filepath = 'sample_annonce_list_pagination.html'
        root_page = get_page_tree(fake_filepath)

        result = lbc.ParsingLeboncoinList.parse(root_page, fake_url)
        urls = sorted(result.urls)

        self.assertEqual(36, len(urls))
        self.assertEqual('https://www.leboncoin.fr/recherche/?category=9&region=22&cities=Grenoble_38000&page=2', urls[0])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1130030581.htm/', urls[1])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1457365725.htm/', urls[-1])

    def test_parse_page_list_last(self):
        fake_url = 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=38190&page=8'
        fake_filepath = 'sample_annonce_list_last.html'
        root_page = get_page_tree(fake_filepath)

        result = lbc.ParsingLeboncoinList.parse(root_page, fake_url)
        urls = sorted(result.urls)

        self.assertEqual(25, len(urls))
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1071666198.htm/', urls[0])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1433979227.htm/', urls[-1])


class TestParserLeboncoin(unittest.TestCase):
    def test_parse_page_info(self):
        fake_url = 'https://www.leboncoin.fr/ventes_immobilieres/1415286514.htm/'
        fake_filepath = 'sample_annonce_estate.html'
        root_page = get_page_tree(fake_filepath)
        result = lbc.ParsingLeboncoinAdEstate.parse(root_page, fake_url)

        self.assertEqual(0, len(result.urls))
        self.assertEqual(1, len(result.ads))
        for url, ad in result.ads.items(): pass
        self.assertEqual(fake_url, url)
        self.assertEqual('01/06/2018', ad.date_creation)
        self.assertEqual(495000, ad.price)
        self.assertEqual('maison', ad.category)
        self.assertEqual(149, ad.surface)
        self.assertEqual(7, ad.rooms)
        self.assertEqual('Le Versoud', ad.location)
        self.assertEqual('CHRISTIAN JOUTY IMMOBILIER', ad.real_estate)


if __name__ == '__main__':
    unittest.main()

