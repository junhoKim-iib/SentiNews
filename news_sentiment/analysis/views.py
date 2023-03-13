from django.shortcuts import render
from .models import StockNews, MainNews, StockSentiment, MainSentiment
from django.core.paginator import Paginator # 페이지네이션을 위한 장고 내장 모듈
from datetime import datetime, timedelta # 날짜 계산을 위한 모듈
from django.views.decorators.cache import cache_page
from .NLP import main_keywords # 키워드 추출 함수
# Create your views here.


# last_week = datetime.now() - timedelta(days=7) # 최근 일주일 날짜

# last_main = MainNews.objects.filter(date__gte=last_week) # 최근 일주일동안의 뉴스 데이터
# # 최근 일주일동안의 감성 분류된 뉴스 데이터 
# main_positive = MainNews.objects.filter(mainsentiment__sentiment= 1 )
# main_negative = MainNews.objects.filter(mainsentiment__sentiment= 2 )
# main_neutral = MainNews.objects.filter(mainsentiment__sentiment= 0 )
# positive_count = main_positive.count()
# negative_count = main_negative.count()
# neutral_count = main_neutral.count()


@cache_page(60 * 15) # 캐시 만료 시간을 15분으로 설정
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
    return render(request, 'analysis/stocks.html', {})




