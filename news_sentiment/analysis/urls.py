# create analysis urls.py

# Path: news_sentiment\analysis\urls.py

from django.urls import path
from . import views

app_name = 'analysis'
urlpatterns = [

    path('', views.home, name='home'),

]