from json import loads


def retrieve_articles(article_indexes):
    articles = []
    for index in article_indexes:
        filename, position = index.split('@')
        with open(filename, 'r', encoding='utf-8') as articles_file:
            articles_file.seek(int(position))
            line = articles_file.readline()
            article = line
            while line[0] != '}':
                line = articles_file.readline()
                article += line
        articles.append(article)
    return articles


class SearchEngine:
    indexes = None
    no_returned_articles = 5

    def __init__(self, no_returned_articles=5):
        with open('../../data/indexes.txt', 'r', encoding='utf-8') as index_file:
            self.indexes = loads(index_file.read())
            self.no_returned_articles = no_returned_articles

    def search_by_keyword(self, keyword):
        if self.indexes and keyword in self.indexes.keys():
            articles_indexes = self.indexes[keyword][:self.no_returned_articles]
            return retrieve_articles(articles_indexes)
        else:
            return []

