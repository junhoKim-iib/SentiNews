from django.db import models
import logging

from django.core.exceptions import ImproperlyConfigured

# import for crawling function 
from .crawler_v1 import get_main_news, get_stock_news
from django.db import IntegrityError

# set logging level to debug
#logging.basicConfig(level=logging.DEBUG)


class StockNews(models.Model):
    subject = models.CharField(max_length=256)
    company = models.CharField(max_length=255)
    date = models.DateField()
    summary = models.TextField()
    content = models.TextField()
    url = models.URLField(unique=True)

    class Meta:
        db_table = 'stock_news'


class MainNews(models.Model):
    subject = models.CharField(max_length=256)
    date = models.DateField()
    content = models.TextField()
    url = models.URLField(unique=True)

    class Meta:
        db_table = 'main_news'



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



#data = get_stock_news('삼성전자', 1)
# insert_stock_news2(data)