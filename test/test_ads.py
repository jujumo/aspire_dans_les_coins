import unittest
from ads.ads import SaleEstate


class TestOffers(unittest.TestCase):
    def test_estate_construct(self):
        args = {
            'url': 'url_pipo',
            'price': 100000,
            'date_grabbed': '13/06/2018',
            'location': 'lancey',
            'zip': 38190,
            'category': 'maison',
            'surface': 130,
        }
        maison = SaleEstate(**args)
        
        for k, v in args.items():
            self.assertEqual(maison.__dict__[k], args[k])


if __name__ == '__main__':
    unittest.main()

