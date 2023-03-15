from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('mypage', views.mypage, name='mypage'),
    path('logout', views.logout_view, name='logout'),
    path('delete_account', views.delete_account, name='delete_account'),
]

