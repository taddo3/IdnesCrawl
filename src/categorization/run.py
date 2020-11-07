from src.categorization.analyzer import Analyzer
from src.categorization.predictor import Predictor
from os import path


file_number = 1
analyzer = Analyzer()

while path.exists('../../data/category_keywords_' + str(file_number) + '.txt'):
    analyzer.make_keywords_statistics('../../data/category_keywords_' + str(file_number) + '.txt')
    file_number += 1

predictor = Predictor(analyzer.category_keyword_score, analyzer.total_keyword_score)

print('Predict category for txt file or cli keywords?\nf - file\nc - command line')
delimiter = input()

if delimiter == 'f':
    print('Write file path: ', end='')
    file_path = input()
    predictor.predict_category_for_file(file_path)
elif delimiter == 'c':
    print('Write keywords: ', end='')
    keywords = input()
    while keywords != 'q':
        keywords = keywords.split()
        predicted_category = predictor.predict_category(keywords)
        print('Predicted category: ' + predicted_category)
        print('\nWrite keyword: ', end='')
        keywords = input()

