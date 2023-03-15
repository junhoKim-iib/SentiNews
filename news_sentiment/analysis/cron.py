# 크롤링 스케쥴링

from datetime import datetime
from .models import MainNews, StockNews,insert_main_news,insert_stock_news
from .crawler_v1 import get_main_news, get_stock_news

def my_scheduled_job():
    # Get today's date in the format "yyyy-mm-dd"
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Crawl main finance news and save to the database
    insert_main_news(get_main_news(date))
    
    # Crawl stock news for Samsung and save to the database
    insert_stock_news(get_stock_news('삼성전자', 10))
 
   
### type the command in the terminal
# python manage.py crontab add