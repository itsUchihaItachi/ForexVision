from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
import json
from datetime import date,timedelta

API_KEY = "taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN"
# vishal = taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN
# ravi = meZyuHiwLZxWD1xaBOPfkHtQx4FiWnuhQQMNxsmLQXrL12YveV

# Create your views here.
def temp(request):
    return render(request,'Base.html')

def home(request):
    amount = request.POST.get('amount')

    base = request.POST.get('baseCurr') # get the base currency symbol from user
    counter = request.POST.get('counterCurr') # get the counter currency symbol from user

    # # Check if the base and counter is not none
    # # After requesting the server and getting data from user

    json_url = urlopen("https://fcsapi.com/api-v2/forex/converter?pair1="+base+"&pair2="+counter+"&amount="+amount+"&access_key="+API_KEY)
    data = json.loads(json_url.read())

    baseindex = "price_1x_"+base
    counterindex = "price_1x_"+counter

    baserate = data['response'][baseindex]
    counterrate = data['response'][counterindex]
    totalAmount = data['response']['total']

    High, Low = HighLow(base, counter)
    lastUpd = lastUpdated(base, counter)
    context = {'totalAmount' : totalAmount,
                'base' : base, 'counter' : counter,
                'counterrate' : counterrate, 'baserate' : baserate,
                'lastUpd' : lastUpd,
                'High' : High, 'Low' : Low }
    return render(request,'Base.html',context)

def HighLow(base, counter):
    today = date.today()
    todayDate = today.strftime("%Y-%m-%d")
    fromDate = today - timedelta(30)

    # https://fcsapi.com/api-v2/forex/history?symbol=EUR/USD&period=1d&from=2020-05-01T12:00&to=2020-11-11T12:00&access_key=taTjcoDno4fAXZKnSBLdvAEKonjHUq3FHdygpJiCwiRYdPKMhN
    json_url = urlopen("https://fcsapi.com/api-v2/forex/history?symbol="+base+"/"+counter+"&period=1d&from="+str(fromDate)+"T12:00&to="+todayDate+"T12:00&access_key="+API_KEY)
    data = json.loads(json_url.read())

    dt = data['response']

    high = []
    low = []

    for ls in dt:
        high.append(ls['h'])
        low.append(ls['l'])

    return max(high), min(low)

def lastUpdated(base, counter):
    json_url = urlopen("https://fcsapi.com/api-v3/forex/latest?symbol="+base+"/"+counter+"&access_key="+API_KEY)
    data = json.loads(json_url.read())

    return data['response'][0]['tm']
    
