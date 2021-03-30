import os

import requests
from bs4 import BeautifulSoup

from settings import DATA_DIR, WEB_PAGES_FILE, DOWNLOADS_PATH


class Crawler:
    def __init__(self, path=DOWNLOADS_PATH, file=WEB_PAGES_FILE):
        self.path = os.path.join(DATA_DIR, path)
        self.file = os.path.join(DATA_DIR, file)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def crawl(self, url):
        response = requests.get(url, allow_redirects=True)
        bs = BeautifulSoup(response.text, 'html.parser')
        print(bs.title.string.replace('/', ' '))
        file = open(os.path.join(self.path, bs.title.string.replace('/', ' ')) + '.txt', 'w', encoding='utf-8')
        file.write(bs.get_text())
        print("Сохранено как {}".format(file.name))
        file.close()

    def download_all(self):
        for url in open(self.file):
            self.crawl(url.split('\n')[0])