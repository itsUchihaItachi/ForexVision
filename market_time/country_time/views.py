from django.shortcuts import render
from django.http import HttpResponse
from .models import market_time
from rest_framework.views import APIView
from django.views.generic import View
from .serializers import TimeSerializer
from rest_framework.response import Response
from .models import market_time
from django.shortcuts import render, redirect


# Create your views here
from django.http import HttpResponse


# Create your views here.

def index(request):

        #radio = request.POST.get('radio')  # radio should be like colm name
        forexs = market_time.objects.all()
        print(forexs)
        return render(request, 'showhours.html', {'forexs': forexs})





