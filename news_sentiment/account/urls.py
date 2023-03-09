from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), #{% url 'home' %} 으로 사용
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('mypage/', views.mypage, name='mypage'),
]

