from django.urls import path

from . import views

urlpatterns = [
    path('',views.temp, name = 'temp'),
    path('ExchangeCurr', views.home, name = 'home'),
    path('charts', views.charts, name = 'charts'),
]