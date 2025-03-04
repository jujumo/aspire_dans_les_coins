import unittest
import argparse, logging
import ads.parsing.ParsingLeboncoin as lbc
from ads.net import get_page_tree, write_content_file

fake_samples = {
    'page_single':
        {'filename': 'sample_annonce_list_nopage.html',
         'url': 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=38420&real_estate_type=1&square=130-max&rooms=4-max&price=min-600000'},
    'page_lot':
        {'filename': 'sample_annonce_list_pagination.html',
         'url': 'https://www.leboncoin.fr/recherche/?category=9&region=22&cities=Grenoble_38000'},
    'page_last':
        {'filename': 'sample_annonce_list_last.html',
         'url': 'https://www.leboncoin.fr/recherche/?category=9&regions=22&location=38190&page=7'},
    'ads':
        {'filename': 'sample_annonce_estate.html',
         'url': 'https://www.leboncoin.fr/ventes_immobilieres/1365750706.htm/'},
}


def build_samples():
    from ads.net import get_content_url
    for page in fake_samples.values():
        logging.info(f'creating sample file {page["filename"]}')
        content = get_content_url(page['url'])
        write_content_file(page['filename'], content)


class TestParserLeboncoinList(unittest.TestCase):
    def test_parse_page_list_url(self):
        fake_url = fake_samples['page_single']['url']
        result = lbc.ParsingLeboncoinList.url_match(fake_url)
        self.assertEqual(result, True)

    def test_parse_page_list_single(self):
        fake_url = fake_samples['page_single']['url']
        fake_filepath = fake_samples['page_single']['filename']
        root_page = get_page_tree(fake_filepath)

        result = lbc.ParsingLeboncoinList.parse(root_page, fake_url)
        urls = sorted(result.urls)

        self.assertEqual(12, len(urls))
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1152536434.htm/', urls[0])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1538837489.htm/', urls[-1])

    def test_parse_page_list_pages(self):
        fake_url = fake_samples['page_lot']['url']
        fake_filepath = fake_samples['page_lot']['filename']
        root_page = get_page_tree(fake_filepath)

        result = lbc.ParsingLeboncoinList.parse(root_page, fake_url)
        urls = sorted(result.urls)

        self.assertEqual(37, len(urls))
        self.assertEqual('https://www.leboncoin.fr/recherche/?category=9&region=22&cities=Grenoble_38000&page=2', urls[0])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1419390087.htm/', urls[1])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1545212209.htm/', urls[-1])

    def test_parse_page_list_last(self):
        fake_url = fake_samples['page_last']['url']
        fake_filepath = fake_samples['page_last']['filename']
        root_page = get_page_tree(fake_filepath)

        result = lbc.ParsingLeboncoinList.parse(root_page, fake_url)
        urls = sorted(result.urls)

        self.assertEqual(6, len(urls))
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1365750706.htm/', urls[0])
        self.assertEqual('https://www.leboncoin.fr/ventes_immobilieres/1518608418.htm/', urls[-1])


class TestParserLeboncoin(unittest.TestCase):
    def test_parse_page_info(self):
        fake_url = fake_samples['ads']['url']
        fake_filepath = fake_samples['ads']['filename']
        root_page = get_page_tree(fake_filepath)
        result = lbc.ParsingLeboncoinAdEstate.parse(root_page, fake_url)

        self.assertEqual(0, len(result.urls))
        self.assertEqual(1, len(result.ads))
        for id, ad in result.ads.items(): pass
        self.assertEqual(1365750706, id)
        self.assertEqual(fake_url, ad.url)
        self.assertEqual('04/11/2018', ad.date_creation)
        self.assertEqual(229000, ad.price)
        self.assertEqual('maison', ad.real_estate_category)
        self.assertEqual(125, ad.surface)
        self.assertEqual(5, ad.rooms)
        self.assertEqual('https://img4.leboncoin.fr/ad-image/18a23bcbbda82fea1ef106c8a003ab440cf5180c.jpg', ad.thumb)
        self.assertEqual('38190', ad.location)
        self.assertEqual('CIMM IMMOBILIER - PONTCHARRA', ad.real_estate_agent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='launch unit test (or build sample files to test against).')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='verbosity level')
    parser.add_argument('-s', '--samples', action='store_true', help='build samples to test against')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    if args.verbose > 1:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.samples:
        build_samples()
    else:
        unittest.main()

