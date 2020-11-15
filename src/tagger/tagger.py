from ufal.morphodita import *
import re
from os import path


class Lemmatizer:

    def __init__(self, morfflex_tagger_filename):
        self.tagger = Tagger.load(morfflex_tagger_filename)
        self.forms = Forms()
        self.lemmas = TaggedLemmas()
        self.tokens = TokenRanges()
        self.tokenizer = self.tagger.newTokenizer()
        self.stopwords = []
        if path.exists('stopwords.txt'):
            with open('stopwords.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    self.stopwords.append(line[:-1])

    def get_lemmas(self, text):
        """
        This method make dict of lemmatized words and its frequency from text and sort this dict by frequency.
        Return sorted dictionary.
        """
        self.tokenizer.setText(text)
        lemmatized_words = dict()

        while self.tokenizer.nextSentence(self.forms, self.tokens):
            self.tagger.tag(self.forms, self.lemmas)
            for lemma in self.lemmas:
                lemmatized_word = re.sub('[-_]+.*|[^\`]+\`[0-9]+', '', lemma.lemma)
                if lemmatized_word and lemmatized_word not in self.stopwords and len(lemmatized_word) > 2:
                    if lemmatized_word in lemmatized_words.keys():
                        lemmatized_words[lemmatized_word] += 1
                    else:
                        lemmatized_words[lemmatized_word] = 1

        return sorted(lemmatized_words.items(), key=lambda x: x[1], reverse=True)
