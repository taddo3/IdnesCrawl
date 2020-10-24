from time import sleep
from random import random
from src.crawler.archive_crawler import ArchiveCrawler
from src.crawler.article_scraper import ArticleScraper

start_url = 'https://www.idnes.cz/zpravy/archiv/'
file_name = '../../data/extracted_articles_1.txt'
max_file_size = 1000000000

crawler = ArchiveCrawler(start_url)
scraper = ArticleScraper(file_name, max_file_size)

page_number = 1
last_page = 1

while page_number <= last_page:
    try:
        crawled_urls = crawler.get_urls(page_number)
        if not crawled_urls:
            print('No urls for page n.' + str(page_number))
            continue
        for url in crawled_urls:
            scraper.scrap_article(url)
            sleep(random())
        page_number += 1

    except Exception as ex:
        print('Error: ' + str(ex))

