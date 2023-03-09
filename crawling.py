import requests
from bs4 import BeautifulSoup
import time
import json
import datetime
import os
stock_list = ["005930", "000660", "035720"] # 삼성전자, SK하이닉스, 카카오

def get_article_list(stock_code, page_num):
    url = f"https://finance.naver.com/item/board.nhn?code={stock_code}&page={page_num}"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    
    articles = []
    
    for tr in soup.select("#content > div.section.inner_sub > table.type2 > tbody > tr"):
        if tr.has_attr("class") and "notice" in tr["class"]:
            continue
        if tr.select_one(".title > a") is None:
            continue
        title = tr.select_one(".title > a").get_text().strip()
        link = "https://finance.naver.com" + tr.select_one(".title > a")["href"]
        author = tr.select_one(".p11").get_text().strip()
        date = tr.select_one(".date").get_text().strip()
        timestamp = datetime.datetime.strptime(date, "%Y.%m.%d %H:%M").timestamp()
        articles.append({
            "title": title,
            "link": link,
            "author": author,
            "date": date,
            "timestamp": timestamp
        })
        print(articles)
    
    return articles


data_dir = "./data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

for stock_code in stock_list:
    article_list = []
    page_num = 1
    
    while True:
        articles = get_article_list(stock_code, page_num)
        if len(articles) == 0:
            break
        article_list += articles
