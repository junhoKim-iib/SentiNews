from django.shortcuts import render
from .models import StockNews, MainNews
from django.core.paginator import Paginator # 페이지네이션을 위한 장고 내장 모듈
# Create your views here.


# def home(request): 
#     main_news = MainNews.objects.all()
#     context = {'main_news': main_news}
#     return render(request, 'analysis/home.html', context)



def home(request):
    news_list = MainNews.objects.all()
    paginator = Paginator(news_list, 10) # 10개의 뉴스를 한 페이지에 보여줍니다.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'analysis/home.html', context)



def stocks(request):
    return render(request, 'analysis/stocks.html', {})

