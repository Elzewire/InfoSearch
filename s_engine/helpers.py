import os
from math import sqrt
from queue import Queue

import requests

from InfoSearch.settings import STATICFILES_DIRS, WEB_PAGES_FILE, WIKI_URL, INDEX_FILE

''' Вспомогательные методы '''


# Генерация случайных ссылок на статьи в википедии
def get_random_wiki_pages(amount=100, file=WEB_PAGES_FILE):
    f = open(os.path.join(STATICFILES_DIRS[0], file), 'w', encoding='utf-8')
    for i in range(amount):
        response = requests.get(WIKI_URL, allow_redirects=True)
        f.write(response.url + '\n')
    f.close()


# Генерация файла index.txt
def index_file(file=INDEX_FILE, web_pages=WEB_PAGES_FILE):
    wp = open(os.path.join(STATICFILES_DIRS[0], web_pages), encoding='utf-8').readlines()
    f = open(os.path.join(STATICFILES_DIRS[0], file), 'w', encoding='utf-8')

    i = 1

    for line in wp:
        f.write('{} {}'.format(i, line))
        i += 1
    f.close()


# Косинусное сходство
def cos_sim(v1, v2):
    len_v1 = sqrt(sum([x * x for x in v1]))
    len_v2 = sqrt(sum([x * x for x in v2]))

    mult = 0
    for x, y in zip(v1, v2):
        mult += x * y

    return mult / (len_v1 * len_v2) if len_v1 * len_v2 != 0 else 0


# Преобразование инфиксного выражения в постфиксное
def bool_statement_to_postfix(statement):
    st_parts = statement.split(' ')
    q = []
    s = []
    for x in st_parts:
        if x == 'OR':
            if len(s) == 0 or s[-1] == '(':
                s.append(x)
            else:
                while len(s) > 0 and s[-1] != '(':
                    q.append(s.pop())
                s.append(x)
        elif x == 'AND':
            if len(s) == 0 or s[-1] == '(':
                s.append(x)
            elif s[-1] == 'OR':
                s.append(x)
            else:
                while s[-1] != '(':
                    q.append(s.pop())
                s.append(x)
        elif x == 'NOT':
            s.append(x)
        elif x == '(':
            s.append(x)
        elif x == ')':
            while len(s) > 0 and s[-1] != '(':
                q.append(s.pop())
            s.pop()
        else:
            q.append(x)
            if len(s) > 0 and s[-1] == 'NOT':
                q.append(s.pop())

    while len(s) > 0:
        q.append(s.pop())

    return q


if __name__ == '__main__':
    x = set(range(10))
    y = set()
    y.add(6)
    print(x)
    print(x.difference(y))