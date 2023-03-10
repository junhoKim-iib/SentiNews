from django.shortcuts import render
from .models import StockNews, MainNews
# Create your views here.
def home(request):

    
    main_news = MainNews.objects.all()
    context = {'main_news': main_news}
    return render(request, 'analysis/home.html', context)


def stocks(request):
    return render(request, 'analysis/stocks.html', {})

