from time import sleep
from random import random
from src.crawler.archive_crawler import ArchiveCrawler
from src.crawler.article_scraper import ArticleScraper

start_url = 'https://www.idnes.cz/zpravy/archiv/'
file_name = '../../data/extracted_articles.txt'

crawler = ArchiveCrawler(start_url)
scraper = ArticleScraper(file_name)

crawled_urls = crawler.get_urls()
for url in crawled_urls:
    scraper.scrap_article(url)
    sleep(random())

