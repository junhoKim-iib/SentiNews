from django.db import models
import logging

from django.core.exceptions import ImproperlyConfigured

# import for crawling function 
from .crawler_v1 import get_main_news
from django.db import IntegrityError


# analysis 
from .NLP import news_analysis

# set logging level to debug
#logging.basicConfig(level=logging.DEBUG)

class News(models.Model):
    subject = models.CharField(max_length=256)
    date = models.DateField()
    content = models.TextField()
    url = models.URLField(unique=True)

    class Meta:
        abstract = True

class StockNews(News):
    company = models.CharField(max_length=255)
    summary = models.TextField()

    class Meta:
        db_table = 'stock_news'


class MainNews(News):
    class Meta:
        db_table = 'main_news'


class MainSentiment(models.Model): 
    # connect to main_news table by url
    news = models.OneToOneField(MainNews, on_delete=models.CASCADE)
    sentiment = models.IntegerField()

    class Meta:
        db_table = 'main_sentiment'


class StockSentiment(models.Model):
    # connect to stock_news table by url
    news = models.OneToOneField(StockNews, on_delete=models.CASCADE)
    sentiment = models.IntegerField()

    class Meta:
        db_table = 'stock_sentiment'



# data: list of news data
# item: dict of news data
# item = {
#     'subject': 'subject',
#     'date': 'date',
#     'content': 'content',
#     'url': 'url',
# }
def insert_main_news(data):
    for item in data:
        try:
            obj = MainNews(subject=item['subject'], date=item['date'], content=item['content'], url=item['url'])
            obj.save()

        except IntegrityError:
            # 이미 저장된 뉴스인 경우 스킵
            continue


def insert_stock_news(data):
    for item in data:
        try:
            obj = StockNews(company=item['company'], subject=item['subject'], date=item['date'], summary=item['summary'], content=item['content'], url=item['url'])
            obj.save()

        except IntegrityError:
            # 이미 저장된 뉴스인 경우 스킵
            continue


def insert_main_sentiment():
    obj_list = news_analysis(MainNews, MainSentiment)# 기간 설정은 함수 내부에서 설정
    for obj in obj_list:
        try:
            obj.save()

        except IntegrityError:
            print('IntegrityError')
            # 이미 저장된 뉴스인 경우 스킵
            continue


def insert_stock_sentiment():
    obj_list = news_analysis(StockNews, StockSentiment)
    for obj in obj_list:
        try:
            obj.save()

        except IntegrityError:
            # 이미 저장된 뉴스인 경우 스킵
            continue



#insert_main_sentiment()










# # one year date list
# import datetime

# start_date = datetime.date(2022, 1, 1)
# end_date = datetime.date(2023, 3, 11)
# delta = datetime.timedelta(days=1)
# dates = [str(start_date + i*delta) for i in range((end_date - start_date).days + 1)]

# for date in dates:
#     data = get_main_news(date)
#     insert_main_news(data)

# data = get_main_news('2021-03-11')
# insert_main_news(data)







