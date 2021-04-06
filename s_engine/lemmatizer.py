import os

import nltk
from pymystem3 import Mystem


def lemmatize(text):
    # Заменить символы пробелами
    text = text.replace('_', ' ')

    # Разбить текст на слова
    tokenizer = nltk.RegexpTokenizer(r"[А-Яа-я]+")
    words = tokenizer.tokenize(text)

    # Лемматизация
    m = Mystem()

    lemmas = m.lemmatize(" ".join(words))
    l2 = []
    for l in lemmas:
        if l != ' ' and l != '\n':
            l2.append(l)

    return words, l2


if __name__ == '__main__':
    path = 'data/downloads/'

    files = os.listdir('data/downloads/')
    for x in files:
        content = open(os.path.join(path, x), encoding='utf-8').read()
        lemmatize(content)
