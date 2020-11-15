import unittest
from src.search.search_engine import SearchEngine
from json import loads


class SearchTestCases(unittest.TestCase):
    def test_search_by_keyword(self):
        engine = SearchEngine(2)
        articles = engine.search_by_keyword('ministr')
        self.assertTrue(bool(articles))
        self.assertEqual(len(articles), 2)
        self.assertNotEqual(loads(articles[0])['title'], loads(articles[1])['title'])

    def test_search_by_keywords(self):
        engine = SearchEngine(2)
        articles_and = engine.search_by_keywords(['ministr', 'Prymula'])
        articles_or = engine.search_by_keywords(['ministr', 'Prymula'], operator='or')
        self.assertTrue(bool(articles_and))
        self.assertTrue(bool(articles_or))
        self.assertEqual(len(articles_and), 2)
        self.assertEqual(len(articles_or), 2)
        self.assertNotEqual(loads(articles_and[0])['title'], loads(articles_and[1])['title'])
        self.assertNotEqual(loads(articles_or[0])['title'], loads(articles_or[1])['title'])


if __name__ == '__main__':
    unittest.main()
