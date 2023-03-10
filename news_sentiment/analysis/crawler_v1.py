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


# crawling main finance news
def get_main_news(date):
    # 날짜 설정
    # date format should be: 'yyyy-mm-dd'
    # 크롤링할 URL 설정
    url = f'https://finance.naver.com/news/mainnews.naver?date={date}'
    # User-Agent 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    # 페이지 요청
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup)
    # 뉴스 기사 리스트 추출
    news_list = soup.select('dd.articleSubject')
    # 뉴스 기사 크롤링
    data = []
    for news in news_list:
        # 뉴스 제목 추출
        title = news.select_one('a').text

        # 뉴스 링크 추출
        link = news.select_one('a')['href']
        link = "https://finance.naver.com" + link 
        # 뉴스 내용 추출
        content_res = requests.get(link, headers=headers)
        content_res.raise_for_status()
        content_soup = BeautifulSoup(content_res.text, 'html.parser')
        content = content_soup.select_one('div#content').text.strip()
        
        item = {'title': title, 'link': link, 'content': content}
        # 결과 출력
        data.append(item)

    return data


# get stock news data.
# name: company name
# max_page: max page number
# return: list of news data
# data = [
#     {
#         'company': 'company',
#         'subject': 'subject',
#         'date': 'date',
#         'summary': 'summary',
#         'content': 'content',
#         'url': 'url',
#     },
#     ...
# ]
# usage: data = get_news('삼성전자', 10)
def get_stock_news(name,max_page):

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
                'company': name,
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


DB_HOST = get_secret("DB_HOST") # database host
DB_DATABASE_NEWS = get_secret("DB_DATABASE_NEWS") # news database
DB_USER = get_secret("DB_USER") # database user
DB_PASSWORD = get_secret("DB_PASSWORD") # database password


# set logging level to debug
#logging.basicConfig(level=logging.DEBUG)

def insert_stock_news(data):
    conn = psycopg2.connect(host=DB_HOST, database=DB_DATABASE_NEWS, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    for item in data:
        cur.execute("INSERT INTO stock_news (company, subject, date, summary, content, url) VALUES (%s, %s, %s, %s, %s, %s)", (item['company'] ,item['subject'], item['date'], item['summary'], item['content'], item['url']))
    conn.commit()
    cur.close()
    conn.close()


# usage:
# data = get_stock_news('에코프로비엠', 1)
# insert_stock_news(data)