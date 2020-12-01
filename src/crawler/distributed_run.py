from time import sleep
from random import random
from src.crawler.archive_crawler import ArchiveCrawler
from src.crawler.article_scraper import ArticleScraper
from src.crawler.another_news_crawler import AnotherCrawler
from src.crawler.another_article_scraper import AnotherScraper
import ray


ray.init()

file_name = '../../data/extracted_articles_1.txt'
max_file_size = 1000000000

crawler1 = ArchiveCrawler('https://www.idnes.cz/zpravy/archiv/')
scraper1 = ArticleScraper(file_name, max_file_size)
crawler2 = AnotherCrawler()
scraper2 = AnotherScraper(file_name, max_file_size)


@ray.remote
def run1():
    urls1 = crawler1.get_urls(1)
    for url1 in urls1:
        scraper1.scrap_article(url1)
        sleep(random())


@ray.remote
def run2():
    urls2 = crawler2.get_urls()
    for url2 in urls2:
        scraper2.scrap_article(url2)
        sleep(random())


task1 = run1.remote()
task2 = run2.remote()

ray.get(task1)
ray.get(task2)

ray.shutdown()

