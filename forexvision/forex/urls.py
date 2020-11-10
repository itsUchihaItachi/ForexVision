from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('Ce',views.home,name = 'home')
]urrency_Exchang