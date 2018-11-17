import unittest
from ads.ads import SaleEstate, to_pandas, from_pandas


class TestOffers(unittest.TestCase):
    def test_estate_construct(self):
        args = {
            'url': 'url_pipo',
            'price': 100000,
            'date_grabbed': '13/06/2018',
            'location': 'lancey',
            'zip': 38190,
            'real_estate_category': 'maison',
            'surface': 130,
        }
        maison = SaleEstate(**args)
        
        for k, v in args.items():
            self.assertEqual(maison.__dict__[k], args[k])


class TestIO(unittest.TestCase):
    def test_to_pandas(self):
        args = {
            'url': 'url_pipo',
            'price': 100000,
            'date_grabbed': '13/06/2018',
            'location': 'lancey',
            'zip': 38190,
            'real_estate_category': 'maison',
            'surface': 130,
        }
        maison = SaleEstate(**args)
        ad_dict = {0: maison}

        df = to_pandas(ad_dict)
        self.assertEqual((1, 8), df.shape)
        row = df.iloc[0]
        for k, a in args.items():
            self.assertEqual(a, row[k])

    def test_from_pandas(self):
        args = {
            'url': 'url_pipo',
            'price': 100000,
            'date_grabbed': '13/06/2018',
            'location': 'lancey',
            'zip': 38190,
            'real_estate_category': 'maison',
            'surface': 130,
        }
        maison = SaleEstate(**args)
        ad_dict = {0: maison}

        df = to_pandas(ad_dict)
        back = from_pandas(df)
        # back = back.iloc[0]
        # for k in args:
        #     self.assertEqual(args[k], back.__dict__[k])
        # print((back))


if __name__ == '__main__':
    unittest.main()

