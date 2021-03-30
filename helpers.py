import os

import requests

from settings import WIKI_URL, WEB_PAGES_FILE, DATA_DIR, INDEX_FILE

''' Вспомогательные методы '''


# Генерация случайных ссылок на статьи в википедии
def get_random_wiki_pages(amount=100, file=WEB_PAGES_FILE):
    f = open(os.path.join(DATA_DIR, file), 'w', encoding='utf-8')
    for i in range(amount):
        response = requests.get(WIKI_URL, allow_redirects=True)
        f.write(response.url + '\n')
    f.close()


# Генерация файла index.txt
def index_file(file=INDEX_FILE, web_pages=WEB_PAGES_FILE):
    wp = open(os.path.join(DATA_DIR, web_pages), encoding='utf-8').readlines()
    f = open(os.path.join(DATA_DIR, file), 'w', encoding='utf-8')

    i = 1

    for line in wp:
        f.write('{} {}'.format(i, line))
        i += 1
    f.close()
