from src.search.search_engine import SearchEngine
from json import dumps, loads
from re import sub
from os import path
from src.categorization.analyzer import Analyzer
from src.categorization.predictor import Predictor


# search initialization
print('Set number of articles you want to return: ', end='')
number = input()
number = int(sub('[^0-9]', '', str(number)))
engine = SearchEngine(number)

# predictor initialization
file_number = 1
analyzer = Analyzer()
while path.exists('../../data/category_keywords_' + str(file_number) + '.txt'):
    analyzer.make_keywords_statistics('../../data/category_keywords_' + str(file_number) + '.txt')
    file_number += 1
predictor = Predictor(analyzer.category_keyword_score, analyzer.total_keyword_score)


print('Write keyword: ', end='')
keyword = input()

while keyword != 'q':

    # articles by keywords search
    keywords = None
    if keyword[0] == '|':
        keywords = sub(' +', ' ', sub('^\| *', '', keyword)).split(' ')
        articles = engine.search_by_keywords(keywords)
    elif keyword[0] == '&':
        keywords = sub(' +', ' ', sub('^\& *', '', keyword)).split(' ')
        articles = engine.search_by_keywords(keywords, operator='and')
    else:
        articles = engine.search_by_keyword(keyword)
    if articles:
        for article in articles:
            print(dumps(loads(article), indent=4, sort_keys=True))
    else:
        print('No articles found.')

    # articles recommendation
    max_recommended_articles = 3 if number > 3 else number
    if not keywords:
        keywords = [keyword]
    new_keywords = predictor.predict_another_keywords(keywords, limit=5)
    recommended_articles = engine.search_by_keywords(new_keywords, operator='and')[:max_recommended_articles]

    while len(recommended_articles) < max_recommended_articles:
        new_keywords.pop()
        if not new_keywords:
            break
        recommended_articles = engine.search_by_keywords(new_keywords, operator='and')[:max_recommended_articles]

    if recommended_articles:
        print('\n\nRecommended articles: ')
        for article in recommended_articles:
            print(dumps(loads(article), indent=4, sort_keys=True))

    # New input = new search
    print('\n\nWrite keyword: ', end='')
    keyword = input()

