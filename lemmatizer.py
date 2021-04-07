import os
import re

import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer


def lemmatize(text):
    lemmas = {}

    # Токенизация
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)

    clean_tokens = []

    # Оставить только русские слова
    pattern = re.compile('[А-Яа-я]+')
    for t in tokens:
        if re.match(pattern, t) is not None:
            clean_tokens.append(t)

    # Убрать стоп-слова
    filtered_tokens = [word for word in clean_tokens if word not in stopwords.words('russian')]

    # Лемматизация
    morph = MorphAnalyzer()
    for token in filtered_tokens:
        lemma = morph.parse(token)
        for l in lemma:
            if l.normal_form not in lemmas.keys():
                lemmas[l.normal_form] = set()
            lemmas[l.normal_form].add(token)

    return tokens, lemmas


if __name__ == '__main__':
    dir = "data/downloads"
    files = os.listdir(dir)
    text = ""
    for f in files:
        text += open(os.path.join(dir, f), 'r', encoding='utf-8').read()

    tokens, lemmas = lemmatize(text)

    t_file = open('data/tokens.txt', 'w', encoding='utf-8')
    for t in tokens:
        t_file.write('{}\n'.format(t))
    t_file.close()

    l_file = open('data/lemmas.txt', 'w', encoding='utf-8')
    for l in lemmas:
        l_file.write('{} {}\n'.format(l, ' '.join(lemmas[l])))
    t_file.close()
