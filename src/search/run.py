from src.search.search_engine import SearchEngine
from json import dumps, loads
from re import sub


print('Set number of articles you want to return: ', end='')
number = input()
number = int(sub('[^0-9]', '', str(number)))
engine = SearchEngine(number)

print('Write keyword: ', end='')
keyword = input()
while keyword != 'q':
    if keyword[0] == '|':
        articles = engine.search_by_keywords(sub(' +', ' ', sub('^\| *', '', keyword)).split(' '))
    elif keyword[0] == '&':
        articles = engine.search_by_keywords(sub(' +', ' ', sub('^\& *', '', keyword)).split(' '), operator='and')
    else:
        articles = engine.search_by_keyword(keyword)
    if articles:
        for article in articles:
            print(dumps(loads(article), indent=4, sort_keys=True))
    else:
        print('No articles found.')
    print('\n\nWrite keyword: ', end='')
    keyword = input()

