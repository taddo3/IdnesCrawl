import operator
from json import loads, dumps
from os import rename, remove


class Predictor:

    def __init__(self, category_keyword_score, total_keyword_score):
        self.category_keyword_score = category_keyword_score
        self.total_keyword_score = total_keyword_score

    def predict_category(self, keywords):
        category_score = dict()
        for category_key in self.category_keyword_score.keys():
            total = 0
            for keyword in keywords:
                total += self.category_keyword_score[category_key][keyword] / self.total_keyword_score[keyword] if \
                    keyword in self.category_keyword_score[category_key] else 0
            category_score[category_key] = total / len(keywords)

        return max(category_score.items(), key=operator.itemgetter(1))[0]

    def predict_category_for_file(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                data = line
                while True:
                    line = f.readline()
                    data += line
                    if line[0] == "}":
                        break
                json_data = loads(data)
                predicted_category = self.predict_category(json_data['keywords'])
                json_data['category'] = predicted_category

                with open(file_name + '_prc', 'a+', encoding='utf-8') as w:
                    w.write(dumps(json_data, indent=4))
                    w.write('\n')

        remove(file_name)
        rename(file_name + '_prc', file_name)

    def predict_another_keywords(self, keywords, limit=5):
        new_keywords = []
        category = self.predict_category(keywords)
        category_keywords = {k: v for k, v in sorted(self.category_keyword_score[category].items(),
                                                     key=lambda item: item[1],
                                                     reverse=True)}
        for keyword in category_keywords:
            if keyword not in keywords:
                new_keywords.append(keyword)
            if len(new_keywords) >= limit:
                break
        return new_keywords

