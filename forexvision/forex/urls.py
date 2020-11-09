from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('Currency_Exchange',views.home,name = 'home')
]