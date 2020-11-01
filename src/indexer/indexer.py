from json import loads, dumps


class Indexer:

    def __init__(self):
        with open('../../data/indexes.txt', 'r', encoding='utf-8') as index_file:
            index_lines = index_file.read()
            if index_lines:
                self.indexes = loads(index_lines)
            else:
                self.indexes = dict()

    def create_index(self, articles_filename, keywords_filename):
        articles_file = open(articles_filename, 'r', encoding='utf-8')
        keywords_file = open(keywords_filename, 'r', encoding='utf-8')

        try:
            while True:
                line = keywords_file.readline()
                if not line or line[0] != '{':
                    break
                article_data = line
                while line[0] != '}':
                    line = keywords_file.readline()
                    article_data += line
                json = loads(article_data)
                position = self.find_position(articles_file, json['title'])

                if position is None:
                    print('Error: Position isn\'t find.')

                if json['keywords'] and position is not None:
                    for keyword in json['keywords']:
                        if keyword in self.indexes.keys():
                            if position not in self.indexes[keyword]:
                                self.indexes[keyword].append(articles_filename + '@' + str(position))
                        else:
                            self.indexes[keyword] = [articles_filename + '@' + str(position)]

            with open('../../data/indexes.txt', 'w', encoding='utf-8') as index_file:
                self.indexes = {k: v for k, v in sorted(self.indexes.items(), key=lambda item: len(item[1]), reverse=True)}
                index_file.write(dumps(self.indexes, indent=4))

        except Exception as ex:
            print('Error: ' + str(ex))
        finally:
            articles_file.close()
            keywords_file.close()

    @staticmethod
    def find_position(articles_file, title):
        while True:
            position = articles_file.tell()
            line = articles_file.readline()
            if not line or line[0] != '{':
                articles_file.seek(0)
                return None
            article_data = line
            while line[0] != '}':
                line = articles_file.readline()
                article_data += line
            json = loads(article_data)
            if json['title'] == title:
                return position

