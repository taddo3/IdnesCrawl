import unittest
from src.categorization.analyzer import Analyzer
from src.categorization.predictor import Predictor


class CategorizationTestCases(unittest.TestCase):
    def test_make_keywords_statistics(self):
        analyzer = Analyzer()
        analyzer.make_keywords_statistics('../../data/category_keywords_1.txt')
        self.assertTrue(bool(analyzer.category_keyword_score))
        self.assertTrue(bool(analyzer.total_keyword_score))

    def test_predict_category(self):
        analyzer = Analyzer()
        analyzer.make_keywords_statistics('../../data/category_keywords_1.txt')
        predictor = Predictor(analyzer.category_keyword_score,
                              analyzer.total_keyword_score)
        category = predictor.predict_category(['ministr', 'Prymula'])
        self.assertEqual(category, 'domaci')
        category = predictor.predict_category(['uchazeč', 'restaurace'])
        self.assertEqual(category, 'ekonomikah')
        category = predictor.predict_category(['Izrael'])
        self.assertEqual(category, 'zahranicni')

    def test_predict_another_keywords(self):
        analyzer = Analyzer()
        analyzer.make_keywords_statistics('../../data/category_keywords_1.txt')
        predictor = Predictor(analyzer.category_keyword_score,
                              analyzer.total_keyword_score)
        keywords = predictor.predict_another_keywords(['ministr', 'Prymula'], limit=3)
        self.assertTrue(bool(keywords))
        self.assertLessEqual(len(keywords), 3)
        self.assertNotIn('ministr', keywords)
        self.assertNotIn('Prymula', keywords)


if __name__ == '__main__':
    unittest.main()
