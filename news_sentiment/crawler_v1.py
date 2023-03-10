# import for crawling 
import urllib
import re
import requests
from bs4 import BeautifulSoup

# import for database
import psycopg2
import logging

 # import for json
import json
from django.core.exceptions import ImproperlyConfigured



# 다른 뉴스 링크.
# https://finance.naver.com/item/news_news.nhn?code=005930&page=1
# ---------------------


# get news data.
# name: company name
# max_page: max page number
# return: list of news data
# data = [
#     {
#         'subject': 'subject',
#         'date': 'date',
#         'summary': 'summary',
#         'content': 'content',
#         'url': 'url',
#     },
#     ...
# ]
# usage: data = get_news('삼성전자', 10)
def get_news(name,max_page):

    data = []
    for page in range(1,max_page + 1):
        url = 'https://finance.naver.com/news/news_search.naver?q={q}&page={page}'
        q_enc = urllib.parse.quote_plus(name, encoding='euc-kr')
        res = requests.get(url.format(q=q_enc, page=page))
        soup = BeautifulSoup(res.text, 'lxml')
        elem_news = soup.select_one('div.newsSchResult dl.newsList')
        elems_subject = elem_news.select('.articleSubject')
        elems_summary = elem_news.select('.articleSummary')
        elems_summary = [re.sub('\s{2,}', ' ', elem_summary.text.strip()) for elem_summary in elems_summary]
        parse_result = urllib.parse.urlparse(url)
        item_url_prefix = '{}://{}'.format(parse_result.scheme, parse_result.netloc)

        for subject, summary in zip(elems_subject, elems_summary):
            item_url = '{}{}'.format(item_url_prefix, subject.a.get('href'))
            subject = subject.text.strip()
            m = re.search(r'\d{4}\-\d{2}\-\d{2}', summary)
            date = ''
            if m is not None:
                date = m.group(0)
            item = {
                'subject': subject,
                'date': date,
                'summary': summary,
                'url': item_url,
            }
            data.append(item)
        for i, item in enumerate(data):
            res = requests.get(item['url'])
            soup = BeautifulSoup(res.text, 'lxml')
            elem_content = soup.select_one('#content')
            elem_content_extra = elem_content.find('div')
            if elem_content_extra:
                elem_content_extra.decompose()
            data[i]['content'] = elem_content.text.strip()
    return data



# insert data to database
# read secrets.json file and connect to database


# read secrets.json to get database connection info

with open("news_sentiment\secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

DB_HOST = get_secret("DB_HOST")
DB_DATABASE = get_secret("DB_DATABASE")
DB_USER = get_secret("DB_USER")
DB_PASSWORD = get_secret("DB_PASSWORD")


# set logging level to debug
#logging.basicConfig(level=logging.DEBUG)

def insert_news_data(data):
    conn = psycopg2.connect(host=DB_HOST, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    for item in data:
        cur.execute("INSERT INTO news (subject, date, summary, content, url) VALUES (%s, %s, %s, %s, %s)", (item['subject'], item['date'], item['summary'], item['content'], item['url']))
    conn.commit()
    cur.close()
    conn.close()


data = get_news('삼성전자', 1)
insert_news_data(data)