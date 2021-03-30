from crawler import Crawler


def crawl(url, path=None):
    if path:
        c = Crawler(path)
    else:
        c = Crawler()
    c.crawl(url)