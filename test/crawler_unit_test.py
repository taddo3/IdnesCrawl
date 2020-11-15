import unittest
import os
from json import loads


class CrawlerTestCases(unittest.TestCase):
    def test_get_urls(self):
        from src.crawler.archive_crawler import ArchiveCrawler
        crawler = ArchiveCrawler('https://www.idnes.cz/zpravy/archiv/')
        urls = crawler.get_urls(1)
        self.assertTrue(bool(urls))
        self.assertLess(20, len(urls))
        urls = crawler.get_urls(10000000)
        self.assertIsNone(urls)

    def test_scrap_article(self):
        from src.crawler.article_scraper import ArticleScraper
        scraper = ArticleScraper('scraper_test.txt', 100000)
        scraper.scrap_article('https://www.idnes.cz/ekonomika/domaci/obceratveni-vydejni-okenko-rozvoz-pruzkum-up-ceska-republika.A201115_110706_ekonomika_misl')
        self.assertTrue(os.path.exists('scraper_test.txt'))
        with open('scraper_test.txt', 'r', encoding='utf-8') as f:
            json = loads(f.read())
        os.remove('scraper_test.txt')
        self.assertTrue(bool(json))
        self.assertIn('title', json.keys())
        self.assertIn('datetime', json.keys())
        self.assertIn('category', json.keys())
        self.assertIn('authors', json.keys())
        self.assertIn('subcategory', json.keys())
        self.assertIn('headline', json.keys())
        self.assertIn('content', json.keys())


if __name__ == '__main__':
    unittest.main()
