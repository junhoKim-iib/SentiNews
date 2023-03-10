from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('home', views.HomeView.as_view(), name='home1'), #{% url 'home' %} 으로 사용
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('mypage', views.mypage, name='mypage'),
    path('logout', views.logout_view, name='logout')
]

