import os

import requests
from bs4 import BeautifulSoup

from InfoSearch.settings import MEDIA_ROOT, DOWNLOADS_PATH

''' Краулер '''


class Crawler:
    def __init__(self, path=DOWNLOADS_PATH):
        # Создание директорий для загрузки
        self.path = os.path.join(MEDIA_ROOT, path)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def crawl(self, url):
        # Загрузка и сохранение страницы по URL
        response = requests.get(url, allow_redirects=True)
        bs = BeautifulSoup(response.text, 'html.parser')
        title = bs.title.string.replace('/', ' ')
        print(title)
        file = open(os.path.join(self.path, bs.title.string.replace('/', ' ')) + '.txt', 'w', encoding='utf-8')
        file.write(bs.get_text())
        print("Сохранено как {}".format(file.name))
        file.close()
        return title, os.path.join(self.path, file.name)
