import unittest
import ads.net as net


class TestUrlChecking(unittest.TestCase):
    def test_is_leboncoin(self):
        # list url
        res = net.is_url('https://www.leboncoin.fr/ventes_immobilieres/offres/rhone_alpes/?th=1&location=Toutes%20les%20communes%2038190&pe=19&sqs=14&ros=4&ret=1')
        self.assertEqual(res, True)
        # ad url
        title = net.get_content_url('https://www.leboncoin.fr/')
        self.assertIsInstance(title, str)


if __name__ == '__main__':
    unittest.main()

