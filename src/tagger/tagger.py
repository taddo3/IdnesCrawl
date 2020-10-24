from ufal.morphodita import *
import re


class Lemmatizer:

    def __init__(self, morfflex_tagger_filename):
        self.tagger = Tagger.load(morfflex_tagger_filename)
        self.forms = Forms()
        self.lemmas = TaggedLemmas()
        self.tokens = TokenRanges()
        self.tokenizer = self.tagger.newTokenizer()
        self.stopwords = []
        with open('stopwords.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                self.stopwords.append(line[:-1])


    def get_lemmas(self, text):
        self.tokenizer.setText(text)
        lemmatized_words = dict()

        while self.tokenizer.nextSentence(self.forms, self.tokens):
            self.tagger.tag(self.forms, self.lemmas)
            for lemma in self.lemmas:
                lemmatized_word = re.sub('[-_]+.*|[^\`]+\`[0-9]+', '', lemma.lemma)
                if lemmatized_word and lemmatized_word not in self.stopwords:
                    if lemmatized_word in lemmatized_words.keys():
                        lemmatized_words[lemmatized_word] += 1
                    else:
                        lemmatized_words[lemmatized_word] = 1

        return sorted(lemmatized_words.items(), key=lambda x: x[1], reverse=True)
