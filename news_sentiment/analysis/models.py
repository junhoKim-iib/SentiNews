from django.db import models


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



# get_main_news() 함수에서 반환하는 데이터를 DB에 저장하는 함수
def insert_main_news(data):
    print("saving main news in DB")
    objs = [MainNews(subject=item['subject'], date=item['date'], content=item['content'], url=item['url']) for item in data]
    MainNews.objects.bulk_create(objs, ignore_conflicts=True)
    print("main news saved in DB")



# get_stock_news() 함수에서 반환하는 데이터를 DB에 저장하는 함수

def insert_stock_news(data):
    print("saving stock news in DB")
    objs = [StockNews(subject=item['subject'], date=item['date'], content=item['content'], url=item['url'], company=item['company'], summary=item['summary']) for item in data]
    StockNews.objects.bulk_create(objs, ignore_conflicts=True)
    print("stock news saved in DB")

    
    




