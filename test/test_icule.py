import net.parser as parser
import unittest


class TestMeta(unittest.TestCase):
    def test_meta(self):
        parser.ParserCollection.parse('leboncoin')


if __name__ == '__main__':
    unittest.main()