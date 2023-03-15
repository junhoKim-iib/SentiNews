from django.shortcuts import render
from .models import StockNews, MainNews, StockSentiment, MainSentiment, \
                    insert_main_news, insert_stock_news
from .crawler_v1 import get_stock_news, get_main_news

from django.core.paginator import Paginator # 페이지네이션을 위한 장고 내장 모듈
from datetime import datetime, timedelta # 날짜 계산을 위한 모듈
from django.views.decorators.cache import cache_page
from .NLP import main_keywords, news_analysis  # 키워드 추출 함수

# Create your views here.



# @cache_page(60 * 15) # 캐시 만료 시간을 15분으로 설정
def home(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # 날짜를 입력받아 해당 기간의 뉴스 데이터를 가져옴
    if start_date and end_date:
        news = MainNews.objects.filter(date__range=[start_date, end_date])

    else: # 날짜를 입력하지 않으면 최근 일주일 데이터를 가져옴
        last_week = datetime.now() - timedelta(days=7) # 최근 일주일 날짜
        news = MainNews.objects.filter(date__gte=last_week) # 최근 일주일동안의 뉴스 데이터


    main_positive = news.filter(mainsentiment__sentiment= 1 )
    main_negative = news.filter(mainsentiment__sentiment= 2 )
    main_neutral = news.filter(mainsentiment__sentiment= 0 )
    positive_count = main_positive.count()
    negative_count = main_negative.count()
    neutral_count = main_neutral.count()

    word_cloud = main_keywords(news) # 최근 일주일동안의 뉴스 키워드 추출

    context = {
        'main_positive': main_positive,
        'main_negative': main_negative,
        'main_neutral': main_neutral,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count':  neutral_count,

        'word_cloud': word_cloud,
 
    }
   
    return render(request, 'analysis/home.html', context)



def stocks(request):
    date = datetime.now().strftime("%Y-%m-%d")
    # if user search stock news then get stock news and show it
    if request.method == 'GET':
        company = request.GET.get('company')
        
        # 뉴스가 존재하고 오늘자 뉴스라면 크롤링을 하지 않음
        if StockNews.objects.filter(company=company).exists() and \
            StockNews.objects.filter(date=date).exists():
            stock_news = StockNews.objects.filter(company=company)

        # 뉴스가 존재하지 않거나 오늘자 뉴스가 아니라면 크롤링을 하고 데이터베이스에 저장
        else:
            insert_stock_news(get_stock_news(company, 3))
        
            news_analysis(date, company)
            stock_news = StockNews.objects.filter(company=company)

        # 감성 분류된 뉴스 데이터
        stock_positive = stock_news.filter(stocksentiment__sentiment= 1 )
        stock_negative = stock_news.filter(stocksentiment__sentiment= 2 )
        stock_neutral = stock_news.filter(stocksentiment__sentiment= 0 )
        positive_count = stock_positive.count()
        negative_count = stock_negative.count()
        neutral_count = stock_neutral.count()

        word_cloud = main_keywords(stock_news) 

        context = {
            'stock_positive': stock_positive,
            'stock_negative': stock_negative,
            'stock_neutral': stock_neutral,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count':  neutral_count,
            'word_cloud': word_cloud,

        }

        return render(request, 'analysis/stocks.html', context)
    

    # if user doesn't search stock news then show main news
    else:
        # 뉴스가 존재하고 오늘자 뉴스라면 크롤링을 하지 않음
        if StockNews.objects.filter(company='삼성전자').exists() and \
            StockNews.objects.filter(date=date).exists():
            stock_news = StockNews.objects.filter(company='삼성전자', date=date)

        else: # 뉴스가 존재하지 않거나 오늘자 뉴스가 아니라면 크롤링을 하고 데이터베이스에 저장
            insert_stock_news(get_stock_news('삼성전자', 3)) # 뉴스 크롤링
            news_analysis(date, '삼성전자') # 감성 분석
            stock_news = StockNews.objects.filter(company='삼성전자', date=date) # 오늘자 뉴스 데이터


        stock_positive = stock_news.filter(stocksentiment__sentiment= 1 )
        stock_negative = stock_news.filter(stocksentiment__sentiment= 2 )
        stock_neutral = stock_news.filter(stocksentiment__sentiment= 0 )
        positive_count = stock_positive.count()
        negative_count = stock_negative.count()
        neutral_count = stock_neutral.count()

        word_cloud = main_keywords(stock_news)

        context = {
            'stock_positive': stock_positive,
            'stock_negative': stock_negative,
            'stock_neutral': stock_neutral,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count':  neutral_count,
            'word_cloud': word_cloud,

        }

        return render(request, 'analysis/stocks.html', context)
      
          

    
    




