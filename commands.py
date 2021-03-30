from crawler import Crawler
from helpers import get_random_wiki_pages, index_file

''' Функции консольных команд '''

# Помощь
def help(params):
    if len(params) == 0:
        print('crawl [URL] - загрузка страницы по URL')
        print('crawl_all - загрузка всех страниц по сгенерированным ссылкам в файле \'web_pages.txt\'')
        print('generate <n> - генерация N ссылок на статьи википедии, по-умолчанию N = 100')
        print('ixfile - создание index.txt файла для сгенерированных статей')
    else:
        print('Неверное число аргументов')


# Загрузка одной страницы краулером
def crawl(params):
    if len(params) == 1:
        print('Идёт загрузка...')
        c = Crawler()
        c.crawl(params[0])
        print('Загрузка завершена')
    else:
        print('Неверное число аргументов')


# Загрузка всех страниц краулером
def crawl_all(params):
    if len(params) == 0:
        print('Идёт загрузка...')
        c = Crawler()
        c.download_all()
        print('Загрузка завершена')
    else:
        print('Неверное число аргументов')


# Генерация ссылок на статьи для загрузки
def generate(params):
    if len(params) == 0:
        print('Идёт генерация...')
        get_random_wiki_pages()
        print('Генерация завершена')
    elif len(params) == 1:
        print('Идёт генерация...')
        get_random_wiki_pages(int(params[0]))
        print('Генерация завершена')
    else:
        print('Неверное число аргументов')


# Генерация файла index.txt
def ixfile(params):
    if len(params) == 0:
        print('Созание файла...')
        index_file()
        print('Файл успешно создан')
    else:
        print('Неверное число аргументов')


COMMANDS = {
    'help': help,
    'crawl': crawl,
    'crawl_all': crawl_all,
    'ixfile': ixfile,
    'generate': generate,
}
