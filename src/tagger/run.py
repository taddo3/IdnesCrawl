from src.tagger.tagger import Lemmatizer
from json import dumps, loads
from os import path
import re


morfflex_tagger_filename = 'czech-morfflex-pdt-161115.tagger'
lemmatizer = Lemmatizer(morfflex_tagger_filename)
no_keywords = 10
file_number = 1


while path.exists('../../data/extracted_articles_' + str(file_number) + '.txt'):
    f = open('../../data/extracted_articles_' + str(file_number) + '.txt', 'r', encoding='utf=8')
    processed_articles = 0

    while True:
        try:
            # Read extracted articles and load as json
            line = f.readline()
            if not line or line[0] != '{':
                break
            article_data = line
            while line[0] != '}':
                line = f.readline()
                article_data += line
            json = loads(article_data)

            # Clean content, lemmatize words, count lemmatized words and store keywords by frequency
            text = re.sub('[\.\,\!\?\'\"\:\“\„\`\(\)\{\}\[\}\%\-\_\*\@\$\+\/\&\|\<\>\;]', '', json['content'])
            text = re.sub(' +', ' ', text)
            sorted_lemmas = lemmatizer.get_lemmas(text)
            keywords = [keyword[0] for keyword in sorted_lemmas[:no_keywords]]
            with open('../../data/articles_keywords_' + str(file_number) + '.txt', 'a+', encoding='utf-8') as k_file:
                k_file.write(dumps({'title': json['title'], 'keywords': keywords}, indent=4, sort_keys=False))
                k_file.write('\n')
            if json['category'] and keywords:
                with open('../../data/category_keywords_' + str(file_number) + '.txt', 'a+', encoding='utf-8') as c_file:
                    c_file.write(dumps({'category': json['category'], 'keywords': keywords}, indent=4, sort_keys=False))
                    c_file.write('\n')

            # This write progress into console after each 100 tagged articles
            processed_articles += 1
            if processed_articles % 100 == 0:
                print('Processed articles: ' + str(processed_articles))

        except Exception as ex:
            print('Error: ' + str(ex))

    file_number += 1
    f.close()






