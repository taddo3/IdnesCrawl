from src.tagger.tagger import Lemmatizer
from json import dumps, loads
from os import path
import re


morfflex_tagger_filename = 'czech-morfflex-pdt-161115.tagger'
lemmatizer = Lemmatizer(morfflex_tagger_filename)
no_keywords = 5
file_number = 1


while path.exists('../../data/extracted_articles_' + str(file_number) + '.txt'):
    f = open('../../data/extracted_articles_' + str(file_number) + '.txt', 'r', encoding='utf=8')

    try:
        while True:
            line = f.readline()
            if not line or line[0] != '{':
                break
            article_data = line
            while line[0] != '}':
                line = f.readline()
                article_data += line
            json = loads(article_data)

            text = re.sub('[\.\,\!\?\'\"\:\“\„\`]', '', json['content'])
            text = re.sub(' +', ' ', text)
            sorted_lemmas = lemmatizer.get_lemmas(text)
            keywords = [keyword[0] for keyword in sorted_lemmas[:no_keywords]]
            with open('../../data/articles_keywords_' + str(file_number) + '.txt', 'a+', encoding='utf-8') as k_file:
                k_file.write(dumps({'title': json['title'], 'keywords': keywords}, indent=4, sort_keys=False))
                k_file.write('\n')
            print('Extracted keywords: ' + str(keywords))

    except Exception as ex:
        print('Error: ' + str(ex))
    finally:
        f.close()
        file_number += 1





