import requests
from crawler import articles_from_pages
from config import cookie
from config import address
from config import token


def post_to_bbs(payload):
    url = address + '/topic/add'
    # payload = {'key1': 'value1', 'key2': 'value2'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        # 直接使用从浏览器中复制下来的 cookie
        'Cookie': cookie
    }
    requests.post(url, data=payload, headers=headers)


def post_articles(articles):
    for article in articles:
        content = '![题图]({0}) 作者 {1} 发布于 {2}\n> {3}\n[原文链接]({4})'.format(
            article.cover_url, article.authors, article.time, article.introduction, article.url
        )
        payload = {
            'board_id': '3',
            'title': article.title,
            'content': content,
            'token': token,
        }
        post_to_bbs(payload)


if __name__ == '__main__':
    post_articles(articles_from_pages(0, 5))
