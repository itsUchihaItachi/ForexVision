from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
import json
from datetime import date,timedelta

# Create your views here.
# def temp(request):
#     return render(request,'Base.html')

def home(request):
    amount = request.POST.get('amount')

    base = request.POST.get('baseCurr') # get the base currency symbol from user
    counter = request.POST.get('counterCurr') # get the counter currency symbol from user

    counterrate = 0
    baserate = 0
    totalAmount = 0
    lastUpdated = 0
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

        lastUpdated = basedata['date']

    Open, Close, High, Low = ohcl(base, counter)
    context = {'totalAmount' : totalAmount,
                'base' : base, 'counter' : counter,
                'counterrate' : counterrate, 'baserate' : baserate,
                'lastUpdated' : lastUpdated,
                'Open' : Open, 'Close' : Close, 'High' : High, 'Low' : Low }
    return render(request,'Base.html',context)

def ohcl(base, counter):
    if base != None and counter != None :
        today = date.today()
        todayDate = today.strftime("%Y-%m-%d")
        fromDate = today - timedelta(30)

        # API_KEY = "taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN"
        # https://fcsapi.com/api-v2/forex/history?symbol=EUR/USD&period=1d&from=2020-05-01T12:00&to=2020-11-11T12:00&access_key=taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN
        json_url = urlopen("https://fcsapi.com/api-v2/forex/history?symbol="+base+"/"+counter+"&period=1d&from="+str(fromDate)+"T12:00&to="+todayDate+"T12:00&access_key=taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN")
        # json_url = urlopen("https://api.exchangeratesapi.io/latest?symbols=USD,GBP")
        data = json.loads(json_url.read())

        dt = data['response']

        opn = []
        close = []
        high = []
        low = []

        for ls in dt:
            opn.append(ls['o'])
            close.append(ls['c'])
            high.append(ls['h'])
            low.append(ls['l'])

        return max(opn), max(close), max(high), max(low)
    else:
        return 0, 0, 0, 0