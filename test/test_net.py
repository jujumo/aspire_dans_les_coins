import unittest
from net.read_net import is_url


class TestUrlChecking(unittest.TestCase):
    def test_is_leboncoin(self):
        # list url
        res = lbc.is_leboncoin('https://www.leboncoin.fr/ventes_immobilieres/offres/rhone_alpes/?th=1&location=Toutes%20les%20communes%2038190&pe=19&sqs=14&ros=4&ret=1')
        self.assertEqual(res, True)
        # ad url
        res = lbc.is_leboncoin('https://www.leboncoin.fr/ventes_immobilieres/1321516937.htm/?ca=22_s')
        self.assertEqual(res, True)
        # not leboncoin
        res = lbc.is_leboncoin('http://www.logic-immo.com/detail-vente-0ae14342-fa2e-6600-1f19-be1b0c57176e.htm?ext=2&mea=orpi')
        self.assertEqual(res, False)
        # a file
        res = lbc.is_leboncoin(r'E:\dev\perso\pa_ploter')
        self.assertEqual(res, False)


if __name__ == '__main__':
    unittest.main()

