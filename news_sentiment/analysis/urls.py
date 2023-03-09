# create analysis urls.py

# Path: news_sentiment\analysis\urls.py

from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [

    path('', views.news_list, name='news_list'),

]