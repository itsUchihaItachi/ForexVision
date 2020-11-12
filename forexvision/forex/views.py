from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
import json

# Create your views here.
def home(request):
    amount = request.POST.get('amount')

    base = request.POST.get('baseCurr') # get the base currency symbol from user
    counter = request.POST.get('counterCurr') # get the counter currency symbol from user

    counterrate = 0
    baserate = 0
    totalAmount = 0

    # Check if the base and counter is not none
    # After requesting the server and getting data from user
    if base != None and counter != None :

        json_urlcounter = urlopen("https://api.exchangeratesapi.io/latest?base=" + base)
        json_urlbase = urlopen("https://api.exchangeratesapi.io/latest?base=" + counter)

        counterdata = json.loads(json_urlcounter.read()) # fetching counter rates in the form of dict
        basedata = json.loads(json_urlbase.read())       # fetching base rates in the form of dict

        # Getting the respective currency rate of counter currency
        for i in counterdata['rates']:
            if i == counter:
                counterrate = counterdata['rates'].get(i)
                break

        for j in basedata['rates']:
            if j == base:
                baserate = basedata['rates'].get(j)
                break

        totalAmount = float(amount) * counterrate  # Calculating total amount
    return render(request,'base.html',{'totalAmount' : totalAmount,'base' : base, 'counter' : counter,  'counterrate' : counterrate, 'baserate' : baserate})



