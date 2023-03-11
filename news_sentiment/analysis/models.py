from django.db import models
import logging

from django.core.exceptions import ImproperlyConfigured

# import for crawling function 
from .crawler_v1 import get_main_news
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


# # one year date list
# import datetime

# start_date = datetime.date(2023, 2, 21)
# end_date = datetime.date(2023, 3, 10)
# delta = datetime.timedelta(days=1)
# dates = [str(start_date + i*delta) for i in range((end_date - start_date).days + 1)]

# for date in dates:
#     data = get_main_news(date)
#     insert_main_news(data)

# data = get_main_news('2021-03-11')
# insert_main_news(data)