from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework import views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
]
