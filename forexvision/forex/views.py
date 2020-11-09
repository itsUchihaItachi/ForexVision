from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    amount = request.POST.get('amount')

    base = request.POST.get('baseCurr')
    counter = request.POST.get('counterCurr')
    return render(request,'base.html',{'amount' : amount, 'baseCurr' : base, 'counterCurr' : counter})


