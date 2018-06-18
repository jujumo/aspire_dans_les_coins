import unittest
import net.parser_leboncoin as lbc


class TestParserLeboncoin(unittest.TestCase):
    def test_parse_page_info(self):
        url = 'sample_annonce_estate.html'
        with open(url, 'r', encoding='utf-8') as html_file:
            content = html_file.read()
        page = lbc.parse_page_estate(content, url)
        self.assertEqual(page.url, url)
        self.assertEqual(page.date_creation, '13/06/2018')
        self.assertEqual(page.price, 479000)
        self.assertEqual(page.category, 'maison')
        self.assertEqual(page.surface, 158)
        self.assertEqual(page.rooms, 6)
        self.assertEqual(page.location, 'Le Versoud')
        self.assertEqual(page.real_estate, 'Barral Immobilier')

    def test_parse_page_list_single(self):
        url = 'sample_annonce_list_nopage.html'
        with open(url, 'r', encoding='utf-8') as html_file:
            content = html_file.read()
        page = lbc.parse_page_list(content, url)

        self.assertEqual(len(page.url_list), 20)
        self.assertEqual(page.url_list[ 0], 'https://www.leboncoin.fr/ventes_immobilieres/1427600032.htm?ca=22_s')
        self.assertEqual(page.url_list[19], 'https://www.leboncoin.fr/ventes_immobilieres/1395426763.htm?ca=22_s')
        self.assertEqual(page.next_url, None)

    def test_parse_page_list_pages(self):
        url = 'sample_annonce_list_pagination.html'
        with open(url, 'r', encoding='utf-8', errors='replace') as html_file:
            content = html_file.read()
        page = lbc.parse_page_list(content, url)

        self.assertEqual(len(page.url_list), 35)
        self.assertEqual(page.url_list[ 0], 'https://www.leboncoin.fr/ventes_immobilieres/1449762236.htm?ca=22_s')
        self.assertEqual(page.url_list[34], 'https://www.leboncoin.fr/ventes_immobilieres/1403357400.htm?ca=22_s')
        self.assertEqual(page.next_url, 'https://www.leboncoin.fr/ventes_immobilieres/offres/rhone_alpes/?o=2&sqs=0&location=Montbonnot-Saint-Martin%2038330')

    def test_parse_page_list_last(self):
        url = 'sample_annonce_list_last.html'
        with open(url, 'r', encoding='utf-8', errors='replace') as html_file:
            content = html_file.read()
        page = lbc.parse_page_list(content, url)

        self.assertEqual(len(page.url_list), 13)
        self.assertEqual(page.url_list[ 0], 'https://www.leboncoin.fr/ventes_immobilieres/1419046932.htm?ca=22_s')
        self.assertEqual(page.url_list[12], 'https://www.leboncoin.fr/ventes_immobilieres/1421855109.htm?ca=22_s')
        self.assertEqual(page.next_url, None)


if __name__ == '__main__':
    unittest.main()

