import os

import requests
from bs4 import BeautifulSoup

from helpers import get_random_wiki_pages, index_file
from settings import DATA_DIR, WEB_PAGES_FILE


class TargetMixin:
    def accept(self, source):
        pass


class SourceMixin:
    def receive(self):
        pass


class Crawler:
    def __init__(self, path='downloads'):
        self.path = os.path.join(DATA_DIR, path)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def crawl(self, url):
        response = requests.get(url, allow_redirects=True)
        bs = BeautifulSoup(response.text, 'html.parser')
        print(bs.title.string)
        file = open(os.path.join(self.path, bs.title.string) + '.txt', 'w', encoding='utf-8')
        file.write(bs.get_text())
        file.close()

    def accept(self, source):
        self.crawl(source)


class FileReader(SourceMixin):
    def __init__(self, file):
        self.file = open(file)
        self.content = self.file.readlines()
        self.file.close()
        self.index = 0

    def readline(self):
        if self.index < len(self.content):
            return self.content[self.index].strip('\n')
        return None

    def receive(self):
        return self.content


class Feeder:
    def __init__(self, target, source):
        self.target = target
        self.source = source

    def feed(self):
        for x in self.source.receive():
            self.target.accept(x)


if __name__ == '__main__':
    #get_random_wiki_pages()
    #r = FileReader(os.path.join(DATA_DIR, WEB_PAGES_FILE))
    #c = Crawler()
    #f = Feeder(c, r)
    #f.feed()
    index_file()
