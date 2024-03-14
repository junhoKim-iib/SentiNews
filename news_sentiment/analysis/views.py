from django.shortcuts import render
from .models import StockNews, MainNews
from datetime import datetime # 날짜 계산을 위한 모듈
from django.views.decorators.cache import cache_page
from .NLP import main_keywords  # 키워드 추출 함수

# Create your views here.


# @cache_page(60 * 15) # 캐시 만료 시간을 15분으로 설정
def home(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print("start date: ",start_date)
    print("end date:", end_date)

    # 날짜를 입력받아 해당 기간의 뉴스 데이터를 가져옴
    # 시작 날짜와 끝 날짜 둘 중 하나만 입력한 경우도 예외처리 해야함.
    if start_date and end_date:
        news = MainNews.objects.filter(date__range=[start_date, end_date]) # 아 여기서 무조건 try로 간다.. 그저 빈 news를 반환할 뿐. 그래서 main_keywords(news)에서 에러가 난다.
        print("check news data length: ",len(news))

    else: # 날짜를 입력하지 않으면 최근 일주일 데이터를 가져옴
        # last_week = datetime.now() - timedelta(days=7) # 최근 일주일 날짜
        # news = MainNews.objects.filter(date__gte=last_week) # 최근 일주일동안의 뉴스 데이터
        news = MainNews.objects.all().order_by('-date')

    main_positive = news.filter(mainsentiment__sentiment= 1 )
    main_negative = news.filter(mainsentiment__sentiment= 2 )
    main_neutral = news.filter(mainsentiment__sentiment= 0 )
    positive_count = main_positive.count()
    negative_count = main_negative.count()
    neutral_count = main_neutral.count()

    # word_cloud = main_keywords(news) # 최근 일주일동안의 뉴스 키워드 추출

    context = {
        'main_positive': main_positive[:10],
        'main_negative': main_negative[:10],
        'main_neutral': main_neutral,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count':  neutral_count,
        # 'word_cloud': word_cloud,
    }
   
    return render(request, 'analysis/home.html', context)


def stocks(request):
    date = datetime.now().strftime("%Y-%m-%d")
    # if user search stock news then get stock news and show it
    
    company = request.GET.get('company')
    if company:
        print('company: ', company)
        
        # Fetch stock news from the database
        stock_news = StockNews.objects.filter(company=company)

        # Sentiment classified news data
        stock_positive = stock_news.filter(stocksentiment__sentiment= 1 )
        stock_negative = stock_news.filter(stocksentiment__sentiment= 2 )
        stock_neutral = stock_news.filter(stocksentiment__sentiment= 0 )
        positive_count = stock_positive.count()
        negative_count = stock_negative.count()
        neutral_count = stock_neutral.count()

        context = {
            'stock_positive': stock_positive[:10],
            'stock_negative': stock_negative[:10],
            'stock_neutral': stock_neutral,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count':  neutral_count,
        }

        return render(request, 'analysis/stocks.html', context)
    
    # if user doesn't search stock news then show main news
    else:
        # Fetch stock news from the database
        stock_news = StockNews.objects.filter(company='삼성전자', date=date)

        stock_positive = stock_news.filter(stocksentiment__sentiment= 1 )
        stock_negative = stock_news.filter(stocksentiment__sentiment= 2 )
        stock_neutral = stock_news.filter(stocksentiment__sentiment= 0 )
        positive_count = stock_positive.count()
        negative_count = stock_negative.count()
        neutral_count = stock_neutral.count()

        context = {
            'stock_positive': stock_positive[:10],
            'stock_negative': stock_negative[:10],
            'stock_neutral': stock_neutral,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count':  neutral_count,
        }

        return render(request, 'analysis/stocks.html', context)
      
          

    
    




