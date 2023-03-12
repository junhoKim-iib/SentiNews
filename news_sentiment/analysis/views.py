from django.shortcuts import render
from .models import StockNews, MainNews, StockSentiment, MainSentiment
from django.core.paginator import Paginator # 페이지네이션을 위한 장고 내장 모듈
from datetime import datetime, timedelta # 날짜 계산을 위한 모듈

from .NLP import main_keywords # 키워드 추출 함수
# Create your views here.


last_week = datetime.now() - timedelta(days=7) # 최근 일주일 날짜

last_main = MainNews.objects.filter(date__gte=last_week) # 최근 일주일동안의 뉴스 데이터
# 최근 일주일동안의 감성 분류된 뉴스 데이터 
main_positive = MainNews.objects.filter(mainsentiment__sentiment= 1 )
main_negative = MainNews.objects.filter(mainsentiment__sentiment= 2 )
main_neutral = MainNews.objects.filter(mainsentiment__sentiment= 0 )

week_keywords = main_keywords(last_main) # 최근 일주일동안의 뉴스 키워드 추출

print(week_keywords)

def home(request):
    
    context = {
        'main_positive': main_positive,
        'main_negative': main_negative,
        'main_neutral': main_neutral,
        'positive_count': main_positive.count(),
        'negative_count': main_negative.count(),
        'neutral_count': main_neutral.count(),

        'week_keywords': week_keywords,
        # 'positive_count': 10,
        # 'negative_count': 4,
        # 'neutral_count': 3,
    
    }
   
    return render(request, 'analysis/home.html', context)



def stocks(request):
    return render(request, 'analysis/stocks.html', {})




