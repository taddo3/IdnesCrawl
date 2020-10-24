from src.indexer.indexer import Indexer
from os import path


file_number = 1
indexer = Indexer()

while path.exists('../../data/extracted_articles_' + str(file_number) + '.txt'):
    indexer.create_index('../../data/extracted_articles_' + str(file_number) + '.txt',
                         '../../data/articles_keywords_' + str(file_number) + '.txt')
    file_number += 1

