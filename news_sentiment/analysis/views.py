from django.shortcuts import render
from .models import StockNews, MainNews, StockSentiment, MainSentiment
from django.core.paginator import Paginator # 페이지네이션을 위한 장고 내장 모듈
from datetime import datetime, timedelta # 날짜 계산을 위한 모듈
# Create your views here.

# def home(request): 
#     main_news = MainNews.objects.all()
#     context = {'main_news': main_news}
#     return render(request, 'analysis/home.html', context)


last_week = datetime.now() - timedelta(days=7) # 최근 일주일 날짜
# 최근 일주일동안의 감성 분류된 뉴스 데이터 
main_positive = MainNews.objects.filter(mainsentiment__sentiment= 1 )
main_negative = MainNews.objects.filter(mainsentiment__sentiment= 2 )
main_neutral = MainNews.objects.filter(mainsentiment__sentiment= 0 )

def home(request):
    
    context = {
        'main_positive': main_positive,
        'main_negative': main_negative,
        'main_neutral': main_neutral,
        # 'positive_count': main_positive.count(),
        # 'negative_count': main_negative.count(),
        # 'neutral_count': main_neutral.count(),
        'positive_count': 10,
        'negative_count': 4,
        'neutral_count': 3,
    
    }
   
    return render(request, 'analysis/home.html', context)



def stocks(request):
    return render(request, 'analysis/stocks.html', {})




