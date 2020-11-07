from json import loads, dumps


class Analyzer:

    def __init__(self):
        self.category_keyword_score = dict()
        self.total_keyword_score = dict()

    def make_keywords_statistics(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as cat_keywords:
            while True:
                line = cat_keywords.readline()
                if not line:
                    break
                data = line

                while True:
                    line = cat_keywords.readline()
                    data += line
                    if not line or line[0] == "}":
                        break

                json_data = loads(data)
                score = 10

                for keyword in json_data['keywords']:
                    if keyword in self.total_keyword_score:
                        self.total_keyword_score[keyword] += score
                    else:
                        self.total_keyword_score[keyword] = score
                    if json_data['category'] not in self.category_keyword_score:
                        self.category_keyword_score[json_data['category']] = dict()
                    if keyword in self.category_keyword_score[json_data['category']]:
                        self.category_keyword_score[json_data['category']][keyword] += score
                    else:
                        self.category_keyword_score[json_data['category']][keyword] = score
                    score -= 1

    def write_keyword_statistics(self):
        with open('category_keyword_score.txt', 'w', encoding='utf-8') as f:
            f.write(dumps(self.category_keyword_score, indent=4, sort_keys=False))
        with open('total_keyword_score.txt', 'w', encoding='utf-8') as f:
            f.write(dumps(self.total_keyword_score, indent=4, sort_keys=False))
