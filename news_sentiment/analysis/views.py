from django.shortcuts import render

# Create your views here.
def news_list(request):
    return render(request, 'news/news_list.html', {})