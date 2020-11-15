import unittest
from json import loads
from os import remove


class IndexerTestCases(unittest.TestCase):
    def test_find_position(self):
        from src.indexer.indexer import Indexer
        position = Indexer.find_position(open('../../data/extracted_articles_1.txt', 'r'), 'Falt\u00fdnek rezignoval na m\u00edstop\u0159edsedu ANO. Poslancem po kobere\u010dku u Babi\u0161e z\u016fst\u00e1v\u00e1 - iDNES.cz')
        self.assertIsNotNone(position)
        position = Indexer.find_position(open('../../data/extracted_articles_1.txt', 'r'), 'Falt')
        self.assertIsNone(position)

    def test_create_index(self):
        from src.indexer.indexer import Indexer
        remove('../../data/indexes.txt')
        i = Indexer()
        i.create_index('../../data/extracted_articles_1.txt', '../../data/articles_keywords_1.txt')
        with open('../../data/indexes.txt', 'r', encoding='utf-8') as index_file:
            data = index_file.read()
            self.assertTrue(bool(data))
            json_data = loads(data)
            self.assertIn('ministr', json_data.keys())


if __name__ == '__main__':
    unittest.main()
