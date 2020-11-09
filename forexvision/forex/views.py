from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    name = request.POST.get('name')
    return render(request,'base.html')