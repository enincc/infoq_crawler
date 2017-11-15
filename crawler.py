import os
import requests
from pyquery import PyQuery as pq


class Model(object):
    """
    基类, 用于显示对象的信息，返回用于 print() 函数的字符串
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Article(Model):
    """
    存储文章信息
    """
    def __init__(self):
        self.title = ''
        self.authors = ''
        self.translators = ''
        self.time = ''
        self.cover_url = ''
        self.introduction = ''
        self.url = ''


def get(url):
    """
    通过 url 获取网页，支持缓存，避免二次下载
    """
    folder = 'cached'
    filename = '{}.html'.format(url.split('articles/', 1)[-1])
    path = os.path.join(folder, filename)
    # 网页文件存在则直接从缓存中获取
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
        return s
    else:
        # 建立缓存文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 发送网络请求, 把获取到的网页写入到文件夹中
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def article_from_div(div):
    """
    从一个 div 里面获取到一篇文章信息
    """
    e = pq(div)
    a = Article()

    a.title = e('h2').text()
    authors_list = e('.authors-list .follow__what')
    a.authors = pq(authors_list[0]).text()
    if len(authors_list) > 1:
        a.translators = pq(authors_list[1]).text()
    a.time = e('.author').text().split(' 发布于', 1)[-1].strip()
    a.cover_url = e('img').attr('src')
    a.introduction = e('p:first-of-type').text()
    a.url = 'http://www.infoq.com' + e('h2 a').attr('href')

    return a


def articles_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有文章
    """
    page = get(url)
    e = pq(page)
    items = e('.news_type1, .news_type2')
    articles = [article_from_div(i) for i in items]
    return articles


def articles_from_pages(start_page=0, pages=5):
    """
    指定抓取的起始页和页数
    """
    articles = []
    for i in range(start_page, start_page+pages):
        url = 'http://www.infoq.com/cn/articles/{}'.format(i*12)
        articles += articles_from_url(url)
    return articles


if __name__ == '__main__':
    print('infoQ articles', articles_from_pages(0, 1))

